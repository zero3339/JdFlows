"""
JDFlows Application Entry Point

This is the main entry point for the JDFlows application.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.main_application import create_application  # noqa: E402


def main() -> int:
    """Main application entry point."""
    try:
        # Create and initialize application
        app = create_application(argv=sys.argv)

        # Run application
        return app.run()

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
