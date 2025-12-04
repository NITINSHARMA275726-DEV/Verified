import time
import random
import sys
import os
from datetime import datetime, timedelta
import itertools
import hashlib

# --- ANSI Color Codes with RGB Support ---
def rgb_color(r, g, b, text):
    """Create RGB colored text."""
    return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

def gradient_text(text, start_color, end_color):
    """Create gradient colored text."""
    colors = []
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    
    for i, char in enumerate(text):
        ratio = i / max(len(text) - 1, 1)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        colors.append(f'\033[38;2;{r};{g};{b}m{char}')
    
    return ''.join(colors) + '\033[0m'

def rainbow_text(text):
    """Create rainbow effect for text."""
    colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]
    
    rainbow = ''
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        rainbow += f'\033[38;2;{color[0]};{color[1]};{color[2]}m{char}'
    rainbow += '\033[0m'
    return rainbow

# Simple ANSI colors for fallback
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
ENDC = '\033[0m'
BOLD = '\033[1m'
BLINK = '\033[5m'
UNDERLINE = '\033[4m'

# --- Configuration ---
MIN_RUN_TIME_SECONDS = 300  # 5 minutes minimum
PAYMENT_AMOUNT = 699
BLUE_TICK_ACTIVATION_MINUTES = 30

# --- Global Variables ---
user_balance = random.randint(10000, 50000)
transaction_id = f"TXN{random.randint(10000000, 99999999)}"
session_start_time = None
instagram_username = ""
instagram_password = ""
holder_name = ""
instagram_data = {}
blue_tick_time = None  # Define globally to fix the error

# --- Special Effects ---
def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.03, color=None):
    """Prints text one character at a time for a dramatic effect."""
    if color:
        sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if color:
        sys.stdout.write(ENDC)
    print()

def rgb_loading_spinner(duration, message="", colors=None):
    """Display a loading spinner with RGB colors."""
    if colors is None:
        colors = [(0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255)]
    
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start_time = time.time()
    color_index = 0
    
    while time.time() - start_time < duration:
        char = spinner_chars[int((time.time() - start_time) * 10) % len(spinner_chars)]
        r, g, b = colors[color_index % len(colors)]
        sys.stdout.write(f"\r\r{rgb_color(r, g, b, char)} {message}")
        sys.stdout.flush()
        time.sleep(0.1)
        color_index += 1
    print()

def progress_bar(percentage, width=50, label="", rgb=False):
    """Display a progress bar with optional RGB."""
    filled = int(width * percentage / 100)
    
    if rgb:
        # RGB gradient progress bar
        r = int(255 * (100 - percentage) / 100)
        g = int(255 * percentage / 100)
        b = 100
        bar = rgb_color(r, g, b, '█' * filled) + '░' * (width - filled)
    else:
        if percentage < 30:
            color = RED
        elif percentage < 70:
            color = YELLOW
        else:
            color = GREEN
        bar = f"{color}{'█' * filled}{ENDC}{'░' * (width - filled)}"
    
    print(f"\r{label}[{bar}] {percentage:3d}%", end="")
    sys.stdout.flush()

# --- Instagram Data Generator (Realistic Simulation) ---
def generate_realistic_instagram_data(username):
    """Generate realistic Instagram data based on username."""
    global instagram_data
    
    # Remove @ if present
    clean_username = username.lstrip('@').lower()
    
    # Use hash of username for consistent but realistic data
    hash_obj = hashlib.md5(clean_username.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # Set seed for consistent results
    random.seed(hash_int)
    
    # Generate realistic data ranges based on username characteristics
    username_length = len(clean_username)
    
    # Account age: 1-10 years (realistic for Instagram)
    years = (hash_int % 10) + 1
    months = (hash_int % 12)
    
    # Generate realistic follower counts
    # Smaller usernames (3-5 chars) get more followers (trendy names)
    if username_length <= 5:
        followers = (hash_int % 1000000) + 50000  # 50k - 1.05M
    elif username_length <= 8:
        followers = (hash_int % 500000) + 10000   # 10k - 510k
    else:
        followers = (hash_int % 100000) + 1000    # 1k - 101k
    
    # Following: typically less than followers
    following = max(50, int(followers * random.uniform(0.1, 0.8)))
    
    # Posts: based on account age and activity level
    posts_per_month = random.randint(3, 30)
    total_posts = min(5000, posts_per_month * (years * 12 + months))
    
    # Engagement rate: realistic ranges
    engagement_rate = round(random.uniform(1.5, 8.5), 2)
    
    # Account categories
    categories = ['Personal', 'Creator', 'Influencer', 'Business', 'Brand', 'Public Figure']
    category = categories[hash_int % len(categories)]
    
    # Bio variations
    bios = [
        f"🌟 {clean_username} | Digital Creator | Content Strategist",
        f"📸 Photography enthusiast | {clean_username}",
        f"🎬 Content Creator | {clean_username}",
        f"💼 Business Account | {clean_username}",
        f"✨ Lifestyle & Travel | {clean_username}",
        f"🎵 Music & Arts | {clean_username}"
    ]
    bio = bios[hash_int % len(bios)]
    
    instagram_data = {
        'username': clean_username,
        'full_name': f"{clean_username.title()} User",
        'followers': f"{followers:,}",
        'following': f"{following:,}",
        'posts': f"{total_posts:,}",
        'account_age': f"{years} year{'s' if years > 1 else ''}, {months} month{'s' if months > 1 else ''}",
        'is_private': (hash_int % 5) == 0,  # 20% chance of being private
        'is_verified': False,
        'engagement_rate': engagement_rate,
        'category': category,
        'bio': bio,
        'avg_likes': f"{int(followers * engagement_rate / 100):,}",
        'avg_comments': f"{int(followers * engagement_rate / 500):,}"
    }
    
    # Reset random seed
    random.seed(time.time())
    
    return instagram_data

# --- Instagram Credentials Handler ---
def get_user_information():
    """Get user information and Instagram credentials."""
    global instagram_username, instagram_password, holder_name, blue_tick_time
    
    print(f"\n\n{'='*80}")
    print(gradient_text("ACCOUNT INFORMATION COLLECTION", (0, 200, 255), (100, 100, 255)))
    print(f"{'='*80}")
    
    # Get holder name with validation
    print(f"\n{rgb_color(255, 215, 0, '[STEP 1/3]')} {BOLD}Personal Information{ENDC}")
    while True:
        name = input(f"{rgb_color(0, 255, 200, 'Enter your full legal name: ')}").strip()
        if len(name.split()) >= 2 and len(name) > 4:
            holder_name = name
            break
        else:
            print(f"{RED}❌ Please enter your full name (first and last name).{ENDC}")
    
    # Get Instagram username with validation
    print(f"\n{rgb_color(255, 215, 0, '[STEP 2/3]')} {BOLD}Instagram Account Verification{ENDC}")
    print(f"{rgb_color(200, 200, 200, 'Enter your real Instagram username for verification.')}")
    
    attempts = 3
    while attempts > 0:
        username = input(f"{rgb_color(0, 255, 200, f'Instagram username (attempt {4-attempts}/3): ')}").strip()
        
        # Clean and validate username
        if username.startswith('@'):
            clean_username = username[1:].strip()
        else:
            clean_username = username.strip()
        
        # Validation checks
        if len(clean_username) < 3:
            print(f"{RED}❌ Username too short. Must be at least 3 characters.{ENDC}")
            attempts -= 1
            continue
        
        if len(clean_username) > 30:
            print(f"{RED}❌ Username too long. Maximum 30 characters.{ENDC}")
            attempts -= 1
            continue
        
        # Check for valid characters
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._")
        if not all(c in valid_chars for c in clean_username):
            print(f"{RED}❌ Invalid characters. Only letters, numbers, dots and underscores allowed.{ENDC}")
            attempts -= 1
            continue
        
        # Check for consecutive dots/underscores
        if '..' in clean_username or '__' in clean_username or '._' in clean_username or '_.' in clean_username:
            print(f"{RED}❌ Invalid username pattern.{ENDC}")
            attempts -= 1
            continue
        
        instagram_username = '@' + clean_username
        
        # Get password
        password = input(f"{rgb_color(0, 255, 200, 'Enter your Instagram password: ')}").strip()
        
        if not password or len(password) < 6:
            print(f"{RED}❌ Password must be at least 6 characters.{ENDC}")
            attempts -= 1
            continue
        
        instagram_password = password
        
        # Simulate credential validation
        print(f"\n{rgb_color(0, 200, 255, '🔐 Validating Instagram credentials...')}")
        rgb_loading_spinner(2, "Checking account authenticity", 
                           [(255, 100, 100), (255, 150, 100), (255, 200, 100)])
        
        # Realistic validation with 85% success rate
        if random.random() < 0.85:
            print(f"{GREEN}✅ Credentials validated successfully!{ENDC}")
            
            # Generate realistic Instagram data
            generate_realistic_instagram_data(clean_username)
            
            # Calculate blue tick activation time
            blue_tick_time = datetime.now() + timedelta(minutes=BLUE_TICK_ACTIVATION_MINUTES)
            
            break
        else:
            print(f"{RED}❌ Username or password is not correct.{ENDC}")
            attempts -= 1
            if attempts > 0:
                print(f"{YELLOW}⚠ You have {attempts} more attempt(s).{ENDC}")
    
    if attempts == 0:
        print(f"\n{RED}❌ Maximum attempts reached. Please restart the verification process.{ENDC}")
        return False
    
    # Save to file
    try:
        with open('user_info.txt', 'w') as f:
            f.write(f"INSTAGRAM BLUE TICK VERIFICATION DATA\n")
            f.write(f"{'='*60}\n")
            f.write(f"Verification Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Account Holder: {holder_name}\n")
            f.write(f"Instagram Username: {instagram_username}\n")
            f.write(f"Verification Status: APPROVED\n")
            f.write(f"Payment Amount: ₹{PAYMENT_AMOUNT}\n")
            f.write(f"Transaction ID: {transaction_id}\n")
            f.write(f"Blue Tick Activation: {blue_tick_time.strftime('%I:%M %p')}\n")
            f.write(f"{'='*60}\n")
            f.write(f"\nACCOUNT STATISTICS:\n")
            f.write(f"{'-'*40}\n")
            for key, value in instagram_data.items():
                if key not in ['is_private', 'is_verified']:
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        
        print(f"\n{GREEN}✅ Information saved to 'user_info.txt'{ENDC}")
        print(f"{CYAN}📁 All verification data has been securely stored.{ENDC}")
        
    except Exception as e:
        print(f"{RED}❌ Could not save information: {e}{ENDC}")
        return False
    
    return True

# --- Virtual Payment ---
def simulate_virtual_payment():
    """Simulate a virtual payment process."""
    global user_balance
    
    print(f"\n\n{'='*80}")
    print(gradient_text("SECURE PAYMENT PROCESSING", (0, 200, 100), (0, 100, 200)))
    print(f"{'='*80}")
    
    print(f"\n{rgb_color(0, 255, 150, '💰 PAYMENT DETAILS:')}")
    print(f"{rgb_color(255, 255, 255, 'Verification Fee:')} {rgb_color(0, 255, 0, f'₹{PAYMENT_AMOUNT}')}")
    print(f"{rgb_color(255, 255, 255, 'Account Holder:')} {rgb_color(255, 215, 0, holder_name)}")
    print(f"{rgb_color(255, 255, 255, 'Instagram Account:')} {rgb_color(0, 200, 255, instagram_username)}")
    print(f"{rgb_color(255, 255, 255, 'Transaction ID:')} {rgb_color(200, 200, 200, transaction_id)}")
    
    # Payment processing
    print(f"\n{rgb_color(0, 200, 255, '🔄 Processing payment...')}")
    rgb_loading_spinner(3, "Connecting to secure payment gateway", 
                       [(0, 150, 255), (50, 200, 255), (100, 255, 255)])
    
    # Animated payment processing
    for i in range(101):
        progress_bar(i, 40, "Payment Authorization ", rgb=True)
        time.sleep(0.20)
    
    print(f"\n\n{rgb_color(0, 255, 0, '✅ PAYMENT SUCCESSFUL!')}")
    print(f"{rgb_color(200, 255, 200, '✓ Amount:')} ₹{PAYMENT_AMOUNT}")
    print(f"{rgb_color(200, 255, 200, '✓ Status:')} {rgb_color(0, 255, 0, 'COMPLETED')}")
    print(f"{rgb_color(200, 255, 200, '✓ Time:')} {datetime.now().strftime('%H:%M:%S')}")
    
    # Receipt
    print(f"\n{rgb_color(255, 215, 0, '📄 PAYMENT RECEIPT:')}")
    print(gradient_text("─" * 50, (100, 100, 255), (200, 100, 255)))
    print(f"{'Service:':<25} {rgb_color(0, 255, 200, 'Blue Tick Verification')}")
    print(f"{'Amount:':<25} {rgb_color(255, 255, 0, f'₹{PAYMENT_AMOUNT}')}")
    print(f"{'Transaction ID:':<25} {rgb_color(200, 200, 255, transaction_id)}")
    print(f"{'Date:':<25} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(gradient_text("─" * 50, (100, 100, 255), (200, 100, 255)))
    
    input(f"\n{rgb_color(0, 255, 150, 'Press ENTER to continue...')}")
    return True

# --- Instagram Account Analysis ---
def analyze_instagram_account():
    """Analyze Instagram account with realistic data."""
    print(f"\n\n{'='*80}")
    print(gradient_text("INSTAGRAM ACCOUNT ANALYSIS", (100, 200, 255), (50, 150, 255)))
    print(f"{'='*80}")
    
    print(f"\n{rgb_color(0, 200, 255, '📊 Analyzing account:')} {rgb_color(255, 215, 0, instagram_username)}")
    
    # Display account statistics
    print(f"\n{rgb_color(0, 255, 200, '🔍 ACCOUNT STATISTICS:')}")
    print(gradient_text("─" * 40, (0, 150, 255), (0, 255, 200)))
    
    stats_display = [
        ("Account Holder", holder_name),
        ("Username", instagram_username),
        ("Followers", instagram_data.get('followers', '0')),
        ("Following", instagram_data.get('following', '0')),
        ("Total Posts", instagram_data.get('posts', '0')),
        ("Account Age", instagram_data.get('account_age', 'N/A')),
        ("Category", instagram_data.get('category', 'N/A')),
        ("Engagement Rate", f"{instagram_data.get('engagement_rate', 0)}%"),
        ("Avg Likes/Post", instagram_data.get('avg_likes', '0')),
        ("Avg Comments/Post", instagram_data.get('avg_comments', '0'))
    ]
    
    for label, value in stats_display:
        print(f"{rgb_color(150, 150, 255, label+':').ljust(25)} {rgb_color(255, 255, 200, value)}")
    
    print(gradient_text("─" * 40, (0, 150, 255), (0, 255, 200)))
    
    # Verification checks
    verification_steps = [
        ("Account Authentication", 99.8),
        ("Content Quality Analysis", 98.5),
        ("Community Guidelines", 99.9),
        ("Identity Verification", 97.2),
        ("Eligibility Assessment", 96.8)
    ]
    
    print(f"\n{rgb_color(0, 255, 150, '🔐 VERIFICATION CHECKS:')}")
    for step, confidence in verification_steps:
        print(f"\n{rgb_color(100, 200, 255, '[CHECK]')} {step}...")
        for i in range(101):
            progress_bar(i, 30, "Analyzing ", rgb=True)
            time.sleep(0.01)
        print(f" {rgb_color(0, 255, 0, '✓')} {rgb_color(200, 255, 200, f'Confidence: {confidence}%')}")
        time.sleep(0.3)
    
    print(f"\n{rgb_color(0, 255, 0, '✅ ACCOUNT ANALYSIS COMPLETE!')}")
    print(f"{rgb_color(200, 255, 200, 'All verification checks passed successfully.')}")
    
    return True

# --- Main Banner ---
def display_banner():
    """Display the main banner."""
    banner = f"""
{BLUE}{BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          ╔═╗┬ ┬┌─┐┌┬┐┬ ┬┌─┐  ╔╦╗┬┌─┐┌─┐┌┬┐┌─┐┬─┐        ║
║          ╠═╝├─┤├─┤ │ ├─┤├┤    ║ ││ │├─┤ │ ├┤ ├┬┘        ║
║          ╩  ┴ ┴┴ ┴ ┴ ┴ ┴└─┘   ╩ ┴└─┘┴ ┴ ┴ └─┘┴└─        ║
║                                                          ║
║             INSTAGRAM VERIFICATION SYSTEM                ║
║                   v6.0 - 'Quantum Pro'                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{ENDC}

{gradient_text("╔══════════════════════════════════════════════════════════╗", (0, 200, 255), (0, 100, 200))}
{gradient_text("║                                                          ║", (0, 200, 255), (0, 100, 200))}
{gradient_text(f"║     Client:        {holder_name if holder_name else 'Verification Client'}              ║", (0, 200, 255), (0, 100, 200))}
{gradient_text(f"║     Session ID:    QVP-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}        ║", (0, 200, 255), (0, 100, 200))}
{gradient_text(f"║     Initiated:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}       ║", (0, 200, 255), (0, 100, 200))}
{gradient_text("║     Status:        VERIFICATION IN PROGRESS              ║", (0, 200, 255), (0, 100, 200))}
{gradient_text("║                                                          ║", (0, 200, 255), (0, 100, 200))}
{gradient_text("╚══════════════════════════════════════════════════════════╝", (0, 200, 255), (0, 100, 200))}

{rgb_color(100, 100, 255, " " * 55 + "System Owner: ")}{rgb_color(255, 215, 0, "Nitin Sharma")}
{rgb_color(100, 100, 255, " " * 55 + "Verified Blue Tick Specialist")}
"""
    print(banner)
    time.sleep(2)

# --- AI Analysis with Risk Assessment ---
def perform_ai_analysis():
    """Perform AI-powered analysis."""
    print(f"\n\n{'='*80}")
    print(gradient_text("ARTIFICIAL INTELLIGENCE ANALYSIS", (200, 100, 255), (150, 50, 200)))
    print(f"{'='*80}")
    
    print_slow(f"\n{rgb_color(0, 255, 150, '[INITIALIZING]')} Neural Network Analysis...", 0.02)
    rgb_loading_spinner(3, "Loading AI analysis models", 
                       [(255, 100, 255), (200, 100, 255), (150, 100, 255)])
    
    ai_tests = [
        ("Behavioral Pattern Analysis", 96.7),
        ("Content Authenticity", 98.2),
        ("Identity Confidence", 99.1),
        ("Risk Assessment", 2.3),  # This is the key low confidence test
        ("Influence Analysis", 94.8),
        ("Social Validation", 97.5)
    ]
    
    for test_name, score in ai_tests:
        print(f"\n{rgb_color(255, 165, 0, '[AI TEST]')} {test_name}...")
        
        # Thinking animation
        for _ in range(3):
            sys.stdout.write(f"\r  {rgb_color(0, 200, 255, 'Analyzing')}{'.' * random.randint(1, 3)}")
            sys.stdout.flush()
            time.sleep(0.2)
        
        # Color code based on score
        if score >= 90:
            color = rgb_color(0, 255, 0, f"{score}% confidence")
        elif score >= 70:
            color = rgb_color(255, 255, 0, f"{score}% confidence")
        else:
            color = rgb_color(255, 50, 50, f"{score}% confidence")
        
        print(f"\r  {test_name}: {color}")
        
        # Special handling for Risk Assessment
        if test_name == "Risk Assessment" and score < 90:
            print(f"  {rgb_color(255, 100, 100, '⚠ Low confidence detected!')}")
            print(f"  {rgb_color(255, 200, 100, '   This may affect verification approval.')}")
            
            # User confirmation
            response = ""
            while response.lower() not in ['y', 'n', 'yes', 'no']:
                response = input(f"  {rgb_color(255, 215, 0, 'Continue verification? (y/n): ')}").strip()
            
            if response.lower() in ['n', 'no']:
                print(f"{RED}[PROCESS TERMINATED] AI analysis aborted.{ENDC}")
                return False
        
        time.sleep(0.5)
    
    print(f"\n{rgb_color(0, 255, 0, '[AI VERDICT]')} Account meets {rgb_color(255, 255, 0, '97.8%')} of verification criteria")
    print(f"{rgb_color(0, 200, 255, '[RECOMMENDATION]')} {BOLD}{rgb_color(0, 255, 0, 'APPROVED')} for Blue Tick verification{ENDC}")
    
    return True

# --- Final Verification Success ---
def display_verification_success():
    """Display final success message."""
    global blue_tick_time
    
    clear_screen()
    
    # Calculate activation time if not already set
    if not blue_tick_time:
        blue_tick_time = datetime.now() + timedelta(minutes=BLUE_TICK_ACTIVATION_MINUTES)
    
    # Epic success display
    print(f"\n\n{gradient_text('╔══════════════════════════════════════════════════════════════════════╗', (0, 100, 255), (0, 200, 255))}")
    print(f"{gradient_text('║                                                                      ║', (0, 100, 255), (0, 200, 255))}")
    
    # Animated success message
    success_messages = [
        "Processing final approval...",
        "Applying verification badge...",
        rgb_color(0, 100, 255, "✅ BLUE TICK ACTIVATED!")
    ]
    
    for msg in success_messages:
        print(f"{' ' * 30}{msg}")
        time.sleep(1)
    
    print(f"{gradient_text('║                                                                      ║', (0, 100, 255), (0, 200, 255))}")
    print(f"{gradient_text('╚══════════════════════════════════════════════════════════════════════╝', (0, 100, 255), (0, 200, 255))}")
    
    time.sleep(1)
    
    # Success Details
    print(f"\n\n{rgb_color(0, 255, 150, '🎉 VERIFICATION SUCCESSFUL! 🎉')}")
    print(f"{rgb_color(200, 255, 200, 'Your Instagram account has been verified.')}")
    
    print(f"\n{rgb_color(255, 215, 0, '📋 VERIFICATION DETAILS:')}")
    print(gradient_text("─" * 50, (0, 150, 255), (0, 255, 150)))
    print(f"{rgb_color(200, 200, 255, 'Account:').ljust(25)} {rgb_color(255, 255, 200, instagram_username)}")
    print(f"{rgb_color(200, 200, 255, 'Holder:').ljust(25)} {rgb_color(255, 255, 200, holder_name)}")
    print(f"{rgb_color(200, 200, 255, 'Status:').ljust(25)} {rgb_color(0, 255, 0, 'VERIFIED ✅')}")
    print(f"{rgb_color(200, 200, 255, 'Score:').ljust(25)} {rgb_color(0, 255, 200, '98.7/100')}")
    print(gradient_text("─" * 50, (0, 150, 255), (0, 255, 150)))
    
    print(f"\n{rgb_color(255, 215, 0, '💰 PAYMENT INFORMATION:')}")
    print(gradient_text("─" * 50, (255, 200, 0), (255, 150, 0)))
    print(f"{rgb_color(200, 255, 200, 'Amount:').ljust(25)} {rgb_color(0, 255, 0, f'₹{PAYMENT_AMOUNT}')}")
    print(f"{rgb_color(200, 255, 200, 'Status:').ljust(25)} {rgb_color(0, 255, 0, 'PAID & CONFIRMED')}")
    print(f"{rgb_color(200, 255, 200, 'Transaction:').ljust(25)} {rgb_color(200, 200, 255, transaction_id)}")
    print(gradient_text("─" * 50, (255, 200, 0), (255, 150, 0)))
    
    print(f"\n{rgb_color(255, 215, 0, '⏰ BLUE TICK ACTIVATION:')}")
    print(gradient_text("─" * 50, (100, 200, 255), (100, 100, 255)))
    print(f"{rgb_color(255, 255, 200, 'Your Blue Tick will be active on:')}")
    print(f"{rgb_color(0, 200, 255, '   ' + blue_tick_time.strftime('%A, %B %d, %Y'))}")
    print(f"{rgb_color(0, 150, 255, '   at ' + blue_tick_time.strftime('%I:%M:%S %p'))}")
    print(f"{rgb_color(200, 200, 255, '   (Current time + 30 minutes)')}")
    print(gradient_text("─" * 50, (100, 200, 255), (100, 100, 255)))
    
    print(f"\n{rgb_color(200, 200, 255, '📁 Verification data saved to:')} {rgb_color(0, 255, 0, 'user_info.txt')}")
    print(f"{rgb_color(200, 200, 255, '🔒 All information is securely stored.')}")
    
    return True

# --- Main Function ---
def main():
    global session_start_time, blue_tick_time
    
    session_start_time = datetime.now()
    clear_screen()
    
    # Initial welcome
    print(f"\n\n{rainbow_text('╔══════════════════════════════════════════════════════════════════════╗')}")
    print(f"{rainbow_text('║             WELCOME TO INSTAGRAM VERIFICATION SYSTEM v6.0              ║')}")
    print(f"{rainbow_text('╚══════════════════════════════════════════════════════════════════════╝')}")
    
    time.sleep(2)
    
    # Step 1: Get user information
    if not get_user_information():
        print(f"\n{RED}❌ Verification process terminated.{ENDC}")
        return
    
    # Display banner with user info
    display_banner()
    
    # Step 2: Analyze Instagram account
    if not analyze_instagram_account():
        print(f"\n{RED}❌ Account analysis failed.{ENDC}")
        return
    
    # Step 3: Virtual Payment
    if not simulate_virtual_payment():
        print(f"\n{RED}❌ Payment processing failed.{ENDC}")
        return
    
    # Step 4: AI Analysis
    print(f"\n\n{'='*80}")
    print(f"{rgb_color(255, 100, 100, '⚠ CRITICAL PHASE: AI ANALYSIS')}")
    print(f"{rgb_color(255, 200, 100, 'Note: Risk Assessment will show 2.3% confidence')}")
    print(f"{rgb_color(255, 200, 100, 'Type \'y\' when prompted to continue.')}")
    print(f"{'='*80}")
    
    time.sleep(3)
    
    if not perform_ai_analysis():
        print(f"\n{RED}❌ AI analysis terminated.{ENDC}")
        return
    
    # Ensure minimum 5-minute runtime
    elapsed_time = (datetime.now() - session_start_time).total_seconds()
    if elapsed_time < MIN_RUN_TIME_SECONDS:
        remaining = MIN_RUN_TIME_SECONDS - elapsed_time
        print(f"\n{rgb_color(255, 215, 0, '[FINALIZING]')} Processing final steps...")
        
        for i in range(int(remaining), 0, -1):
            minutes = i // 60
            seconds = i % 60
            sys.stdout.write(f"\r{rgb_color(0, 200, 255, '[SYNCING]')} Time remaining: {minutes:02d}:{seconds:02d}")
            sys.stdout.flush()
            time.sleep(1)
        print()
    
    # Final Success
    display_verification_success()
    
    # Session Statistics
    print(f"\n\n{'='*80}")
    print(gradient_text("SESSION STATISTICS", (255, 100, 100), (200, 50, 50)))
    print(f"{'='*80}")
    
    end_time = datetime.now()
    duration = (end_time - session_start_time).total_seconds()
    
    stats = [
        ("Start Time", session_start_time.strftime('%H:%M:%S')),
        ("End Time", end_time.strftime('%H:%M:%S')),
        ("Duration", f"{int(duration // 60)}m {int(duration % 60)}s"),
        ("Instagram Account", instagram_username),
        ("Account Holder", holder_name),
        ("Payment Amount", f"₹{PAYMENT_AMOUNT}"),
        ("Verification Score", "98.7/100"),
        ("Blue Tick Activation", blue_tick_time.strftime('%I:%M %p') if blue_tick_time else "N/A"),
        ("Transaction ID", transaction_id),
        ("Data File", " Good✅")
    ]
    
    for idx, (label, value) in enumerate(stats):
        r = 100 + (idx * 20) % 155
        g = 100 + (idx * 15) % 155
        b = 200 + (idx * 10) % 55
        print(f"  {rgb_color(r, g, b, f'{label}:').ljust(25)} {rgb_color(0, 150, 255, value)}")
    
    print(f"\n{rainbow_text('✨ VERIFICATION PROCESS COMPLETE! ✨')}")
    print(f"{rgb_color(0, 255, 200, 'Your Blue Tick will be visible within 30 minutes.')}")
    print(f"{rgb_color(200, 255, 200, 'Thank you for choosing our verification service.')}")
    
    print(f"\n{rgb_color(100, 100, 255, '─' * 80)}")
    print(f"{rgb_color(200, 200, 255, 'System Owner: ')}{rgb_color(255, 215, 0, 'Nitin Sharma')}")
    print(f"{rgb_color(200, 200, 255, 'Contact: support@bluetick-verify.com')}")
    print(f"{rgb_color(200, 200, 255, '24/7 Support Available')}")
    print(f"{rgb_color(100, 100, 255, '─' * 80)}\n")

# --- Run the script ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}❌ Verification process interrupted.{ENDC}")
        print(f"{YELLOW}⚠ Partial data may be saved to user_info.txt{ENDC}")
        sys.exit(0)