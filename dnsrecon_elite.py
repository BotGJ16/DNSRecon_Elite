#!/usr/bin/env python3
"""
DNSRecon Elite - Enhanced DNS Reconnaissance Tool
A modern, powerful yet simple DNS subdomain scanner
Author: Enhanced from dnscan by Suna.so
"""

import asyncio
import aiohttp
import argparse
import json
import sys
import time
from datetime import datetime
from typing import List, Dict, Any
import dns.resolver
import dns.zone
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for cross-platform colored output
colorama.init()

class Colors:
    """Color constants for beautiful output"""
    HEADER = Fore.CYAN
    OKBLUE = Fore.BLUE
    OKGREEN = Fore.GREEN
    WARNING = Fore.YELLOW
    FAIL = Fore.RED
    ENDC = Style.RESET_ALL
    BOLD = Style.BRIGHT

class DNSReconElite:
    """Elite DNS reconnaissance tool with modern features"""
    
    def __init__(self):
        self.results = []
        self.stats = {
            'total_queries': 0,
            'successful': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None
        }
        
    def print_banner(self):
        """Display beautiful banner"""
        banner = f"""
{Colors.HEADER}
╔═══════════════════════════════════════════════════════════════╗
║                    DNSRecon Elite v1.0                        ║
║         Enhanced DNS Reconnaissance Tool                      ║
║                                                               ║
║  🔍 Discover • 🛡️ Secure • ⚡ Fast • 🎨 Beautiful             ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
        print(banner)
    
    def print_status(self, message, status_type="info"):
        """Print status messages with colors"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if status_type == "info":
            print(f"{Colors.OKBLUE}[{timestamp}] ℹ️  {message}{Colors.ENDC}")
        elif status_type == "success":
            print(f"{Colors.OKGREEN}[{timestamp}] ✅ {message}{Colors.ENDC}")
        elif status_type == "warning":
            print(f"{Colors.WARNING}[{timestamp}] ⚠️  {message}{Colors.ENDC}")
        elif status_type == "error":
            print(f"{Colors.FAIL}[{timestamp}] ❌ {message}{Colors.ENDC}")
    
    async def check_zone_transfer(self, domain: str) -> List[str]:
        """Check for zone transfer vulnerability"""
        self.print_status(f"Checking zone transfer for {domain}")
        
        try:
            # Get nameservers
            ns_records = dns.resolver.resolve(domain, 'NS')
            zone_data = []
            
            for ns in ns_records:
                ns_name = str(ns).rstrip('.')
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_name, domain))
                    for name, node in zone.nodes.items():
                        zone_data.append(str(name))
                    self.print_status(f"Zone transfer successful from {ns_name}", "success")
                    return zone_data
                except Exception:
                    continue
                    
            return []
        except Exception as e:
            self.print_status(f"Zone transfer check failed: {str(e)}", "warning")
            return []
    
    async def get_dns_records(self, domain: str) -> Dict[str, List[str]]:
        """Get all DNS records for a domain"""
        records = {
            'A': [],
            'AAAA': [],
            'CNAME': [],
            'MX': [],
            'TXT': [],
            'NS': []
        }
        
        for record_type in records.keys():
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(answer) for answer in answers]
            except:
                pass
                
        return records
    
    async def brute_force_subdomains(self, domain: str, wordlist: List[str], threads: int = 10) -> List[Dict[str, Any]]:
        """Brute force subdomains with async support"""
        self.print_status(f"Starting subdomain brute force with {len(wordlist)} entries")
        
        found_subdomains = []
        semaphore = asyncio.Semaphore(threads)
        
        async def check_subdomain(subdomain):
            async with semaphore:
                full_domain = f"{subdomain}.{domain}"
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.timeout = 2
                    resolver.lifetime = 2
                    
                    # Check A record
                    answers = resolver.resolve(full_domain, 'A')
                    ips = [str(answer) for answer in answers]
                    
                    if ips:
                        found_subdomains.append({
                            'subdomain': full_domain,
                            'ips': ips,
                            'type': 'A'
                        })
                        self.print_status(f"Found: {full_domain} -> {', '.join(ips)}", "success")
                        
                except Exception:
                    pass
        
        # Create tasks for all subdomains
        tasks = [check_subdomain(sub) for sub in wordlist]
        await asyncio.gather(*tasks)
        
        return found_subdomains
    
    def load_wordlist(self, filename: str) -> List[str]:
        """Load subdomain wordlist"""
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            # Default wordlist if file not found
            return ['www', 'mail', 'ftp', 'admin', 'api', 'blog', 'shop', 'dev', 'test']
    
    def generate_report(self, domain: str, results: Dict[str, Any]) -> str:
        """Generate beautiful report"""
        report = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}
{Colors.HEADER}║                        DNS RECON REPORT                       ║{Colors.ENDC}
{Colors.HEADER}╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.BOLD}Target Domain:{Colors.ENDC} {domain}
{Colors.BOLD}Scan Date:{Colors.ENDC} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{Colors.BOLD}Total Subdomains Found:{Colors.ENDC} {len(results.get('subdomains', []))}

{Colors.OKGREEN}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}
{Colors.OKGREEN}║                        DNS RECORDS                            ║{Colors.ENDC}
{Colors.OKGREEN}╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        
        # DNS Records
        for record_type, values in results.get('dns_records', {}).items():
            if values:
                report += f"\n{Colors.BOLD}{record_type} Records:{Colors.ENDC}\n"
                for value in values:
                    report += f"  • {value}\n"
        
        # Subdomains
        if results.get('subdomains'):
            report += f"""
{Colors.OKBLUE}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}
{Colors.OKBLUE}║                      SUBDOMAINS FOUND                         ║{Colors.ENDC}
{Colors.OKBLUE}╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
            for sub in results['subdomains']:
                report += f"\n{Colors.BOLD}• {sub['subdomain']}{Colors.ENDC}\n"
                report += f"  IPs: {', '.join(sub['ips'])}\n"
        
        # Statistics
        report += f"""
{Colors.WARNING}╔═══════════════════════════════════════════════════════════════╗{Colors.ENDC}
{Colors.WARNING}║                        STATISTICS                             ║{Colors.ENDC}
{Colors.WARNING}╚═══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        report += f"Total Queries: {self.stats['total_queries']}\n"
        report += f"Successful: {self.stats['successful']}\n"
        report += f"Failed: {self.stats['failed']}\n"
        report += f"Scan Duration: {self.stats['end_time'] - self.stats['start_time']:.2f} seconds\n"
        
        return report
    
    async def run_scan(self, domain: str, wordlist_file: str = None, threads: int = 10) -> Dict[str, Any]:
        """Run complete DNS reconnaissance scan"""
        self.print_banner()
        self.stats['start_time'] = time.time()
        
        results = {
            'domain': domain,
            'dns_records': {},
            'subdomains': [],
            'zone_transfer': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Get DNS records
        self.print_status("Gathering DNS records...")
        results['dns_records'] = await self.get_dns_records(domain)
        
        # Check zone transfer
        self.print_status("Checking for zone transfer...")
        zone_data = await self.check_zone_transfer(domain)
        results['zone_transfer'] = zone_data
        
        # Brute force subdomains
        wordlist = self.load_wordlist(wordlist_file) if wordlist_file else self.load_wordlist('subdomains.txt')
        self.stats['total_queries'] = len(wordlist)
        
        subdomains = await self.brute_force_subdomains(domain, wordlist, threads)
        results['subdomains'] = subdomains
        self.stats['successful'] = len(subdomains)
        self.stats['failed'] = self.stats['total_queries'] - self.stats['successful']
        
        self.stats['end_time'] = time.time()
        
        return results

def main():
    """Main function with beautiful CLI interface"""
    parser = argparse.ArgumentParser(
        description='DNSRecon Elite - Enhanced DNS Reconnaissance Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
{Colors.HEADER}Examples:{Colors.ENDC}
  {Colors.OKGREEN}dnsrecon_elite.py -d example.com{Colors.ENDC}
  {Colors.OKGREEN}dnsrecon_elite.py -d example.com -w custom_wordlist.txt{Colors.ENDC}
  {Colors.OKGREEN}dnsrecon_elite.py -d example.com -t 20{Colors.ENDC}
  {Colors.OKGREEN}dnsrecon_elite.py -d example.com -o results.json{Colors.ENDC}
        '''
    )
    
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('-w', '--wordlist', help='Custom wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('-o', '--output', help='Output file (JSON format)')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    if args.no_color:
        # Disable colors
        colorama.deinit()
        colorama.init(strip=True)
    
    # Run scan
    scanner = DNSReconElite()
    
    async def run():
        try:
            results = await scanner.run_scan(args.domain, args.wordlist, args.threads)
            
            # Print report
            report = scanner.generate_report(args.domain, results)
            print(report)
            
            # Save to file if specified
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(results, f, indent=2)
                scanner.print_status(f"Results saved to {args.output}", "success")
                
        except KeyboardInterrupt:
            scanner.print_status("Scan interrupted by user", "warning")
        except Exception as e:
            scanner.print_status(f"Error: {str(e)}", "error")
    
    # Run async
    asyncio.run(run())

if __name__ == "__main__":
    main()
