# Testing

- Test compile this template using SNES-IDE, if it works, it was successfully installed in your system!

- You can also test in build with this function:

```python
def test() -> None:
    """
    Test the project.
    """
    install_bat = SNESIDEOUT / "INSTALL.bat"

    if install_bat.exists():

        try:
            subprocess.run([str(install_bat)], check=True, shell=True, cwd=SNESIDEOUT)

        except subprocess.CalledProcessError as e:

            print(f"INSTALL.bat failed with exit code {e.returncode}")

    else:
        
        print("INSTALL.bat not found in SNES-IDE-out directory.")
```
