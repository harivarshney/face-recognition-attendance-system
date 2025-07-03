# Face Recognition Attendance System

A modern Python-based face recognition attendance system using OpenCV and Tkinter GUI.

## 🎯 Features

- **Student Registration**: Capture and store student face data
- **Real-time Face Recognition**: Automatic attendance marking
- **Professional GUI**: Modern dark-themed interface
- **Password Protection**: Secure model training
- **Attendance Reports**: Daily attendance tracking in CSV format
- **Multi-camera Support**: Works with built-in or external cameras

## 📋 Requirements

- Python 3.7+
- OpenCV
- NumPy
- Pandas
- Pillow (PIL)
- Tkinter (usually included with Python)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/face-recognition-attendance.git
   cd face-recognition-attendance
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
face-recognition-attendance/
├── main.py                           # Main application file
├── camera_test.py                    # Camera testing utility
├── test_dependencies.py              # Dependency verification
├── requirements.txt                  # Python dependencies
├── haarcascade_frontalface_default.xml  # Face detection model
├── README.md                         # This file
├── .gitignore                        # Git ignore rules
├── Attendance/                       # Daily attendance records (auto-created)
├── StudentDetails/                   # Student information (auto-created)
├── TrainingImage/                    # Face training images (auto-created)
└── TrainingImageLabel/              # Trained model files (auto-created)
```

## 🎯 How to Use

### 1. Register Students
- Enter student ID and name
- Click "Take Images"
- Position face in camera frame
- System captures 100+ face samples automatically
- Press 'q' to stop early

### 2. Train the Model
- Click "Train Model"
- Set password when prompted (first time)
- Wait for training completion

### 3. Track Attendance
- Click "Track Attendance" 
- Camera opens for real-time recognition
- Attendance automatically recorded when faces are recognized
- Press 'q' to stop tracking

## 🔧 Troubleshooting

### Camera Issues
1. **Run camera test:**
   ```bash
   python camera_test.py
   ```

2. **Check camera permissions:**
   - Windows: Settings > Privacy > Camera
   - Make sure "Allow apps to access camera" is enabled

3. **Close other applications** using the camera (Skype, Teams, etc.)

### Common Problems
- **"No camera found"**: Check camera connections and permissions
- **"Haarcascade file missing"**: Ensure the XML file is in the project directory
- **Poor face detection**: Ensure good lighting conditions

## 📊 Output Files

- `StudentDetails/StudentDetails.csv` - Student information database
- `Attendance/Attendance_YYYY-MM-DD.csv` - Daily attendance records
- `TrainingImageLabel/Trainner.yml` - Trained face recognition model

## 🛡️ Security Features

- Password-protected model training
- Secure student data storage
- Input validation and error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Python community for excellent libraries
- Contributors and testers

---


