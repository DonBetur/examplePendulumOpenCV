import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import numpy as np
import pytube


def estimatePose(corners, marker_size, mtx, distortion):
    marker_points = np.array(
        [
            [-marker_size / 2, marker_size / 2, 0],
            [marker_size / 2, marker_size / 2, 0],
            [marker_size / 2, -marker_size / 2, 0],
            [-marker_size / 2, -marker_size / 2, 0],
        ],
        dtype=np.float32,
    )
    trash = []
    rvecs = []
    tvecs = []
    i = 0
    for c in corners:
        nada, R, t = cv2.solvePnP(
            marker_points, corners[i], mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE
        )
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash


url = "https://youtu.be/ZjjecqEfPtM"
youtube = pytube.YouTube(url)
video = youtube.streams.get_highest_resolution()
video.download()

# Generate an ArUCo marker
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
marker_image = np.zeros((200, 200), dtype=np.uint8)
marker_id = 5
cv2.aruco.generateImageMarker(aruco_dict, marker_id, 200, marker_image, 1)
cv2.imwrite("marker.png", marker_image)

# Perform motion tracking on a video
video_file = "metronomDZ.mp4"
cap = cv2.VideoCapture(video_file)

marker_size = 0.05  # Size of the marker in meters
camera_matrix = np.array(
    [[1000, 0, 320], [0, 1000, 240], [0, 0, 1]]
)  # Example camera matrix

poses = []  # List to store the marker poses

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    parameters = cv2.aruco.DetectorParameters()

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    marker_corners, marker_ids, _ = detector.detectMarkers(frame)

    if marker_ids is not None:
        rvecs, tvecs, trashes = estimatePose(
            marker_corners, marker_size, camera_matrix, None
        )

        for rvec, tvec in zip(rvecs, tvecs):
            pose = np.hstack((rvec, tvec))
            poses.append(pose)

    aruco.drawDetectedMarkers(frame, marker_corners, marker_ids)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Perform post-processing with plots
rotations = [abs(pose[:, 0]) for pose in poses]
translations = [pose[:, 1] for pose in poses]


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

ax1.plot(rotations)
ax1.set_title("Marker Rotations")
ax1.set_xlabel("Frame")
ax1.set_ylabel("Rotation")

ax2.plot(translations)
ax2.set_title("Marker Translations")
ax2.set_xlabel("Frame")
ax2.set_ylabel("Translation")

plt.tight_layout()
plt.savefig("results.png")
plt.show()
