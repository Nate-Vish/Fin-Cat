"""
Validation functions for FinCat setup and configuration.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Tuple, List

import anthropic
import yaml
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

logger = logging.getLogger('fincat.validators')


def validate_python_version() -> Tuple[bool, str]:
    """
    Validate Python version is 3.8 or higher.

    Returns:
        Tuple of (is_valid, message)
    """
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"❌ Python 3.8+ required, found {version.major}.{version.minor}.{version.micro}"


def validate_config_file(config_path: str = 'config/config.yaml') -> Tuple[bool, str]:
    """
    Validate config.yaml exists and is valid YAML.

    Args:
        config_path: Path to config file

    Returns:
        Tuple of (is_valid, message)
    """
    config_file = Path(config_path)

    if not config_file.exists():
        return False, f"❌ Config file not found: {config_path}"

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Validate required sections
        required_sections = ['folders', 'ai', 'excel', 'processing']
        missing = [s for s in required_sections if s not in config]

        if missing:
            return False, f"❌ Config missing sections: {missing}"

        return True, f"✅ Config file valid"

    except yaml.YAMLError as e:
        return False, f"❌ Invalid YAML syntax: {e}"
    except Exception as e:
        return False, f"❌ Error reading config: {e}"


def validate_env_file(env_path: str = 'config/.env') -> Tuple[bool, str]:
    """
    Validate .env file exists and has API key.

    Args:
        env_path: Path to .env file

    Returns:
        Tuple of (is_valid, message)
    """
    env_file = Path(env_path)

    if not env_file.exists():
        return False, (
            f"❌ .env file not found\n"
            f"   Fix: cp config/.env.example config/.env\n"
            f"   Then edit config/.env and add your API key"
        )

    # Check if API key is set
    api_key = None
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('ANTHROPIC_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

    if not api_key or api_key == '' or 'your-key-here' in api_key.lower():
        return False, (
            f"❌ ANTHROPIC_API_KEY not set in {env_path}\n"
            f"   Get key from: https://console.anthropic.com/\n"
            f"   Add to config/.env: ANTHROPIC_API_KEY=sk-ant-your-key-here"
        )

    return True, "✅ .env file exists with API key"


def validate_api_key() -> Tuple[bool, str]:
    """
    Validate Anthropic API key by making a test call.

    Returns:
        Tuple of (is_valid, message)
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        return False, (
            "❌ ANTHROPIC_API_KEY environment variable not set\n"
            "   Make sure you ran: source venv/bin/activate"
        )

    try:
        # Make minimal test call
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1,
            messages=[{"role": "user", "content": "Hi"}]
        )

        return True, "✅ API key valid (test call successful)"

    except anthropic.AuthenticationError:
        return False, (
            "❌ API key invalid (401 authentication error)\n"
            "   Get new key from: https://console.anthropic.com/\n"
            "   Update config/.env: ANTHROPIC_API_KEY=sk-ant-your-key-here"
        )
    except anthropic.APIError as e:
        return False, f"❌ API error: {e}"
    except Exception as e:
        return False, f"❌ Unexpected error validating API: {e}"


def validate_folders(config: dict) -> Tuple[bool, str]:
    """
    Validate all required folders exist or can be created.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        folders = config['folders']
        required_folders = ['data', 'input', 'processed', 'logs']

        for folder_key in required_folders:
            folder_path = Path(folders[folder_key])
            folder_path.mkdir(parents=True, exist_ok=True)

        return True, "✅ All folders created/validated"

    except Exception as e:
        return False, f"❌ Error creating folders: {e}"


def run_full_validation(verbose: bool = False) -> bool:
    """
    Run all validation checks and report results.

    Args:
        verbose: Show detailed output

    Returns:
        True if all validations pass, False otherwise
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}FinCat v2.0 - Setup Validation")
    print(f"{Fore.CYAN}{'='*60}\n")

    checks = [
        ("Python Version", validate_python_version),
        ("Config File", validate_config_file),
        (".env File", validate_env_file),
    ]

    results = []
    messages = []

    # Run checks that don't require config first
    for check_name, check_func in checks:
        if verbose:
            print(f"Checking {check_name}...")

        is_valid, message = check_func()
        results.append(is_valid)
        messages.append((check_name, message))

        # Print result
        if is_valid:
            print(f"{Fore.GREEN}{message}")
        else:
            print(f"{Fore.RED}{message}")

    # If basic checks pass, load config and run remaining checks
    if all(results):
        try:
            from .config import load_config
            config = load_config()

            # Additional checks
            additional_checks = [
                ("Folders", lambda: validate_folders(config)),
                ("API Key", validate_api_key),
            ]

            for check_name, check_func in additional_checks:
                if verbose:
                    print(f"\nChecking {check_name}...")

                is_valid, message = check_func()
                results.append(is_valid)
                messages.append((check_name, message))

                if is_valid:
                    print(f"{Fore.GREEN}{message}")
                else:
                    print(f"{Fore.RED}{message}")

        except Exception as e:
            results.append(False)
            print(f"{Fore.RED}❌ Error loading configuration: {e}")

    # Summary
    print(f"\n{Fore.CYAN}{'='*60}")
    if all(results):
        print(f"{Fore.GREEN}✅ All checks passed! FinCat is ready to use.")
        print(f"\n{Fore.CYAN}Next steps:")
        print(f"  1. Test: {Fore.WHITE}python -m fincat.main --test")
        print(f"  2. Run:  {Fore.WHITE}python -m fincat.main")
    else:
        print(f"{Fore.RED}❌ Some checks failed. Please fix the issues above.")
        print(f"\n{Fore.YELLOW}Need help? Check the README or run with --verbose")
    print(f"{Fore.CYAN}{'='*60}\n")

    return all(results)


def print_fix_instructions(check_name: str, error_message: str):
    """Print helpful fix instructions for common errors."""
    instructions = {
        'config': "Run: cp config/config.yaml.example config/config.yaml",
        'env': "Run: cp config/.env.example config/.env\nThen edit and add your API key",
        'api': "Get API key from: https://console.anthropic.com/\nAdd to config/.env",
    }

    print(f"\n{Fore.YELLOW}💡 How to fix:")
    for key, instruction in instructions.items():
        if key in check_name.lower():
            print(f"{Fore.WHITE}   {instruction}")
            break
