import cv2
import numpy as np
from skimage.feature import local_binary_pattern

IMG_SIZE = (128, 128)


def extract_features(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    img = cv2.resize(img, IMG_SIZE)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = []

    for i in range(3):
        hist = cv2.calcHist([img], [i], None, [8], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        features.extend(hist)

    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size
    features.append(edge_density)

    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    features.append(laplacian_var)

    for i in range(3):
        channel = img[:, :, i]
        features.append(channel.mean())
        features.append(channel.std())

    lbp = local_binary_pattern(gray, P=8, R=1, method="uniform")
    lbp_hist, _ = np.histogram(lbp, bins=10, range=(0, 10))
    lbp_hist = lbp_hist / (lbp_hist.sum() + 1e-6)
    features.extend(lbp_hist)

    h, w = edges.shape
    quadrants = [
        edges[0:h // 2, 0:w // 2], edges[0:h // 2, w // 2:w],
        edges[h // 2:h, 0:w // 2], edges[h // 2:h, w // 2:w],
    ]
    for q in quadrants:
        features.append(np.sum(q > 0) / q.size)

    return np.array(features, dtype=np.float32)