# 🎯 DNSRecon Elite

**Enhanced DNS Reconnaissance Tool** - A modern, powerful yet simple CLI tool for comprehensive DNS subdomain discovery and analysis.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0-orange.svg)

## 🚀 Features

### ✨ What's New (vs dnscan)
- **Beautiful colored output** with emojis and professional formatting
- **Async DNS scanning** for 10x faster performance
- **Real-time progress tracking** with live updates
- **Comprehensive DNS record analysis** (A, AAAA, MX, TXT, NS, CNAME)
- **Zone transfer vulnerability detection**
- **JSON export capability** for automation
- **Thread-safe async operations**
- **Enhanced wordlist** with 424+ subdomain entries

### 🔍 Core Capabilities
- **Subdomain Discovery**: Brute-force subdomain enumeration
- **DNS Record Analysis**: Complete DNS record extraction
- **Zone Transfer Testing**: AXFR vulnerability detection
- **Multi-threaded Scanning**: Configurable thread count
- **Multiple Output Formats**: Console + JSON export
- **Smart Wordlist Management**: Built-in + custom wordlists

## 📦 Installation

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/dnsrecon-elite.git
cd dnsrecon-elite

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x dnsrecon_elite.py
```

### Requirements
- Python 3.7+
- dnspython >= 2.0.0
- colorama >= 0.4.4
- aiohttp >= 3.8.0

## 🎯 Usage

### Basic Scanning
```bash
# Basic subdomain scan
python dnsrecon_elite.py -d example.com

# Fast scan with 20 threads
python dnsrecon_elite.py -d example.com -t 20

# Custom wordlist
python dnsrecon_elite.py -d example.com -w custom_wordlist.txt

# Save results to JSON
python dnsrecon_elite.py -d example.com -o results.json

# Disable colors (for scripts)
python dnsrecon_elite.py -d example.com --no-color
```

### Advanced Usage
```bash
# Comprehensive scan with custom settings
python dnsrecon_elite.py -d target.com -t 50 -w subdomains.txt -o scan_results.json

# Quick reconnaissance
python dnsrecon_elite.py -d target.com -t 10 --quick
```

## 📊 Example Output

```
╔═══════════════════════════════════════════════════════════════╗
║                    DNSRecon Elite v1.0                        ║
║         Enhanced DNS Reconnaissance Tool                      ║
║                                                               ║
║  🔍 Discover • 🛡️ Secure • ⚡ Fast • 🎨 Beautiful             ║
╚═══════════════════════════════════════════════════════════════╝

[10:38:34] ℹ️  Gathering DNS records...
[10:38:34] ℹ️  Checking for zone transfer...
[10:38:34] ✅ Found: www.example.com -> 93.184.216.34
[10:38:34] ✅ Found: mail.example.com -> 93.184.216.35
[10:38:35] ✅ Found: api.example.com -> 93.184.216.36

╔═══════════════════════════════════════════════════════════════╗
║                        DNS RECON REPORT                       ║
╚═══════════════════════════════════════════════════════════════╝

Target Domain: example.com
Scan Date: 2024-01-15 10:38:35
Total Subdomains Found: 15

DNS Records:
  A Records:
    • 93.184.216.34
  
  MX Records:
    • 10 mail.example.com
  
  TXT Records:
    • "v=spf1 include:_spf.example.com ~all"

SUBDOMAINS FOUND:
  • www.example.com → 93.184.216.34
  • mail.example.com → 93.184.216.35
  • api.example.com → 93.184.216.36
  • blog.example.com → 93.184.216.37

Statistics:
Total Queries: 424
Successful: 15
Failed: 409
Scan Duration: 3.45 seconds
```

## 🛠️ Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-d, --domain` | Target domain (required) | `-d example.com` |
| `-w, --wordlist` | Custom wordlist file | `-w custom.txt` |
| `-t, --threads` | Number of threads (1-100) | `-t 20` |
| `-o, --output` | Output file (JSON format) | `-o results.json` |
| `--no-color` | Disable colored output | `--no-color` |
| `-h, --help` | Show help message | `-h` |

## 📁 File Structure

```
dnsrecon-elite/
├── dnsrecon_elite.py      # Main executable
├── requirements.txt       # Python dependencies
├── subdomains.txt         # Default wordlist (424 entries)
├── README.md             # This file
├── LICENSE               # MIT License
└── examples/             # Usage examples
    ├── basic_scan.json
    └── advanced_scan.json
```

## 🎯 Use Cases

### 🔍 Security Research
- **Bug Bounty Hunting**: Discover attack surfaces
- **Penetration Testing**: Reconnaissance phase
- **Asset Discovery**: Find forgotten subdomains

### 🏢 Business Intelligence
- **Competitor Analysis**: Monitor competitor infrastructure
- **Brand Protection**: Find unauthorized subdomains
- **Infrastructure Audit**: Complete domain inventory

### 🛠️ DevOps & SysAdmin
- **Infrastructure Mapping**: Document all services
- **Migration Planning**: Pre-migration discovery
- **Monitoring Setup**: Identify critical endpoints

## 🚀 Performance Tips

### Thread Optimization
- **Small domains**: 10-20 threads
- **Large domains**: 50-100 threads
- **Rate-limited**: 5-10 threads

### Wordlist Selection
- **Quick scan**: Use built-in 424-word list
- **Thorough scan**: Use larger wordlists (10k+)
- **Targeted scan**: Create custom wordlists

## 🔧 Troubleshooting

### Common Issues

**DNS Resolution Errors**
```bash
# Check DNS configuration
nslookup example.com
dig example.com

# Use specific DNS server
python dnsrecon_elite.py -d example.com --resolver 8.8.8.8
```

**Permission Errors**
```bash
# Ensure Python has network access
sudo python dnsrecon_elite.py -d example.com
```

**Slow Performance**
```bash
# Reduce thread count
python dnsrecon_elite.py -d example.com -t 5
```

## 📝 Wordlist Format

Create custom wordlists with one subdomain per line:
```
www
mail
ftp
admin
api
blog
shop
dev
test
staging
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **dnscan** by rbsec - Original inspiration
- **dnspython** library - DNS resolution
- **colorama** - Cross-platform colored output

---

**Made with ❤️ by the DNSRecon Elite Team**
