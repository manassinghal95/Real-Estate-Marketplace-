import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

uri = "mongodb+srv://nishant:12345@cluster0.r5rerfn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client =

def insert_alert(direction, start_time, end_time):
    alert = {
        "direction": direction,
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
        "duration_seconds": (end_time - start_time).total_seconds()
    }
    collection.insert_one(alert)
    print(f"Alert sent for {direction} after {alert_duration} seconds.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    start = time.time()

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)  # Flipped for selfie view
    image.flags.writeable = False

    results = face_mesh.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape
    face_2d = []
    face_3d = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [33, 263, 1, 61, 291, 199]:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])

            # Get 2D Coord
            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_length = 1 * img_w
            cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                   [0, focal_length, img_w / 2],
                                   [0, 0, 1]])
            distortion_matrix = np.zeros((4, 1), dtype=np.float64)

            success, rotation_vec, translation_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, distortion_matrix)

            # Getting rotational of face
            rmat, jac = cv2.Rodrigues(rotation_vec)
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360

            # Determine head pose direction
            if y < -alert_threshold:
                text = "Looking Left"
                if left_tilt_start_time is None:
                    left_tilt_start_time = time.time()
                elif not alert_active and (time.time() - left_tilt_start_time) > alert_duration:
                    alert_active = True
                    alert_start_time = datetime.now()
                    cv2.putText(image, "ALERT: Looking Left!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            else:
                if alert_active and left_tilt_start_time is not None:
                    alert_end_time = datetime.now()
                    insert_alert("left", alert_start_time, alert_end_time)
                    alert_active = False
                left_tilt_start_time = None

            if y > alert_threshold:
                text = "Looking Right"
                if right_tilt_start_time is None:
                    right_tilt_start_time = time.time()
                elif not alert_active and (time.time() - right_tilt_start_time) > alert_duration:
                    alert_active = True
                    alert_start_time = datetime.now()
                    cv2.putText(image, "ALERT: Looking Right!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            else:
                if alert_active and right_tilt_start_time is not None:
                    alert_end_time = datetime.now()
                    insert_alert("right", alert_start_time, alert_end_time)
                    alert_active = False
                right_tilt_start_time = None

            if -alert_threshold <= y <= alert_threshold:
                text = "Forward"
                if alert_active:
                    alert_end_time = datetime.now()
                    insert_alert("forward", alert_start_time, alert_end_time)
                    alert_active = False
                left_tilt_start_time = None
                right_tilt_start_time = None

            nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rotation_vec, translation_vec, cam_matrix, distortion_matrix)
            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

            cv2.line(image, p1, p2, (255, 0, 0), 3)
            cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            cv2.putText(image, "x: " + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "y: " + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    end = time.time()
    totalTime = end - start
    fps = 1 / totalTime
    cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    mp_drawing.draw_landmarks(image=image,
                              landmark_list=face_landmarks,
                              connections=mp_face_mesh.FACEMESH_CONTOURS,
                              landmark_drawing_spec=drawing_spec,
                              connection_drawing_spec=drawing_spec)
    cv2.imshow('Head Pose Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
client.close()



# //sasxyyyyyyyyyyyyyyclea
