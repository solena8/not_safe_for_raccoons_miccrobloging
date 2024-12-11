from PIL import Image, ImageChops
import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
from playwright.sync_api import Page, expect

class Test_UI:

    def _make_login_snapshot(self, page: Page, server_url: str):
        page.goto(server_url)
        page.evaluate("document.activeElement.blur()")
        page.screenshot(path="snapshots/login_reference.png")


    def test_login_snapshot(self, page, test_server):
        server_url = test_server.url
        self._make_login_snapshot(page, server_url)
        reference_snapshot_path = "snapshots/login_reference.png"
        page.goto(server_url)
        page.evaluate("document.activeElement.blur()")  # Supprime le focus actif
        page.screenshot(path="snapshots/login_actual.png")
        actual_snapshot_path="snapshots/login_actual.png"

        # Comparaison des images
        assert self.compare_snapshots(actual_snapshot_path, reference_snapshot_path), "Les images ne correspondent pas"
        page.close()

    def compare_snapshots(self, image1_path, image2_path):
        image1_path = os.path.abspath(image1_path)
        image2_path = os.path.abspath(image2_path)

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
