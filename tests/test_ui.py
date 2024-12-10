from PIL import Image, ImageChops

def test_make_login_snapshot(browser):
    page = browser.new_page()
    page.goto("http://127.0.0.1:8000")
    page.evaluate("document.activeElement.blur()")  # Supprime le focus actif
    page.screenshot(path="snapshots/login_reference.png")
    page.close()


def test_login_snapshot(browser):
    page = browser.new_page()
    page.goto("http://127.0.0.1:8000")
    reference_snapshot_path = "snapshots/login_reference.png"

    page.evaluate("document.activeElement.blur()")  # Supprime le focus actif
    page.screenshot(path="snapshots/login_actual.png")
    actual_snapshot_path="snapshots/login_actual.png"

    # Comparaison des images
    assert compare_snapshots(actual_snapshot_path, reference_snapshot_path), "Les images ne correspondent pas"
    page.close()

def compare_snapshots(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    diff = ImageChops.difference(image1, image2)

    if diff.getbbox():
        print("Images are different!")
        diff_path = "snapshots/differences.png"
        diff.save(diff_path)
        print(f"Différences sauvegardées dans {diff_path}")
        return False
    else:
        print("Images are identical!")
        return True
