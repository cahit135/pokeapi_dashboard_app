import subprocess
import sys

def main():
    try:
        # This runs 'streamlit run homepage.py' exactly as if you typed it
        subprocess.run(["streamlit", "run", "./dashboard/Homepage.py"], check=True)
    except KeyboardInterrupt:
        # Handles graceful exit when you press Ctrl+C
        print("\nDashboard closed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()