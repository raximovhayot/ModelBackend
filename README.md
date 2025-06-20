# DDoS Aniqlash Tizimi

Tarmoq trafigidagi DDoS (Distributed Denial of Service) hujumlarini aniqlash va tasniflash uchun mashina o'rganishidan foydalanuvchi veb-ilova.

## Xususiyatlar

- **Real vaqt rejimida aniqlash**: DDoS hujumlarini aniqlash uchun tarmoq trafigi ma'lumotlarini real vaqt rejimida tahlil qilish
- **Ko'p sinfli tasniflash**: Turli xil DDoS hujumlarini (Syn, UDP, LDAP va boshqalar) aniqlash
- **Interaktiv boshqaruv paneli**: Tarmoq trafigi va hujum statistikasini vizualizatsiya qilish
- **Tarixiy ma'lumotlar**: Tarixiy tarmoq ma'lumotlari va aniqlanishlarni ko'rish va filtrlash
- **REST API**: RESTful API orqali tarmoq ma'lumotlarini qabul qilish va bashoratlarni qaytarish

## Arxitektura

Ilova quyidagi komponentlardan iborat:

### Backend
- **REST API**: Tarmoq ma'lumotlarini qabul qiladi va bashoratlarni qaytaradi
- **Bashorat xizmati**: Tarmoq trafigini tasniflash uchun Random Forest modelidan foydalanadi
- **Ma'lumotlar bazasi**: Tarmoq ma'lumotlari va bashorat natijalarini saqlaydi
- **WebSocket Server**: UI ga real vaqt rejimida yangilanishlarni taqdim etadi
- **Queue Service**: Bashorat vazifalarini navbatga qo'yish va qayta ishlash
- **Utils**: Umumiy funksionallik va yordamchi funksiyalar

### Frontend
- **Boshqaruv paneli**: Real vaqt rejimida tarmoq trafigi va hujum aniqlanishini ko'rsatadi
- **Tarix**: Tarixiy tarmoq ma'lumotlari va aniqlanishlarni ko'rsatadi
- **Grafiklar**: Aniqlash statistikasi va tendentsiyalarini vizualizatsiya qiladi

## O'rnatish

### Talablar
- Python 3.8 yoki undan yuqori
- pip (Python paket menejeri)

### O'rnatish

1. Repozitoriyani klonlash:
   ```
   git clone <repository-url>
   cd ddos_detection_app
   ```

2. Bog'liqliklarni o'rnatish:
   ```
   pip install -r requirements.txt
   ```

3. O'qitilgan model faylini (`random_forest_model.pkl`) ilova katalogiga joylashtiring.

4. Ilovani ishga tushiring:

   Faqat Flask ilovasini ishga tushirish uchun:
   ```
   python app.py
   ```

   Faqat worker jarayonini ishga tushirish uchun:
   ```
   python worker.py
   ```

   Flask ilovasi va worker jarayonini bir vaqtda ishga tushirish uchun:
   ```
   python run.py
   ```

5. Ilovaga veb-brauzeringizda `http://localhost:5000` orqali kiring

### Docker bilan o'rnatish

1. Repozitoriyani klonlash:
   ```
   git clone <repository-url>
   cd ddos_detection_app
   ```

2. Docker Compose yordamida ilovani ishga tushiring:
   ```
   docker-compose up -d
   ```

3. Ilovaga veb-brauzeringizda `http://localhost:5000` orqali kiring

4. Ilovani to'xtatish uchun:
   ```
   docker-compose down
   ```

#### Docker muhitini sozlash

Docker Compose fayli quyidagi xizmatlarni o'z ichiga oladi:

- **app**: Asosiy ilova (Flask va worker jarayonlari)
- **redis**: Navbat xizmati uchun Redis

Muhitni sozlash uchun `docker-compose.yml` faylidagi environment o'zgaruvchilarini o'zgartiring.

### Batafsil o'rnatish yo'riqnomasi

Ilovani o'rnatish va ishga tushirish bo'yicha batafsil yo'riqnoma uchun [DEPLOYMENT.md](DEPLOYMENT.md) fayliga qarang. Bu hujjat mahalliy va Docker o'rnatish, ishlab chiqarish muhitiga o'rnatish va muammolarni bartaraf etish bo'yicha batafsil ma'lumotlarni o'z ichiga oladi.

## Foydalanish

### Boshqaruv paneli

Boshqaruv paneli real vaqt rejimida tarmoq trafigi tahlili va DDoS hujumlarini aniqlanishini ko'rsatadi. U quyidagilarni o'z ichiga oladi:

- Tafsilotlar bilan so'nggi aniqlash
- Aniqlash statistikasi grafigi
- So'nggi aniqlanishlar jadvali

### Tarix

Tarix sahifasi tarixiy tarmoq ma'lumotlari va aniqlanishlarni ko'rish va filtrlash imkonini beradi:

1. Filtrlarni tanlang (hujum turi, limit)
2. Natijalarni yangilash uchun "Filtrlarni qo'llash" tugmasini bosing
3. Ma'lumot tugmasini bosib, aniqlash tafsilotlarini ko'ring

### API

Ilova tarmoq ma'lumotlarini qabul qilish va bashoratlar qilish uchun REST API taqdim etadi:

#### Endpointlar

- `POST /api/network-data`: Bashorat uchun tarmoq ma'lumotlarini yuborish
- `GET /api/network-data/list`: Barcha tarmoq ma'lumotlarini olish
- `GET /api/network-data/<id>`: ID bo'yicha tarmoq ma'lumotlarini olish
- `GET /api/network-data/label/<label>`: Bashorat qilingan yorliq bo'yicha tarmoq ma'lumotlarini olish

#### So'rov namunasi

```json
POST /api/network-data
Content-Type: application/json

{
  "protocol": 6,
  "flow_duration": 1234,
  "total_fwd_packets": 10,
  "total_backward_packets": 5,
  "fwd_packets_length_total": 1500.0,
  "bwd_packets_length_total": 500.0,
  "fwd_packet_length_max": 150.0,
  "fwd_packet_length_min": 60.0,
  "fwd_packet_length_std": 20.0,
  "bwd_packet_length_max": 100.0,
  "bwd_packet_length_min": 40.0,
  "flow_bytes_per_s": 1000.5,
  "flow_packets_per_s": 10.5,
  "bwd_packets_per_s": 5.0,
  "flow_iat_mean": 100.0,
  "flow_iat_min": 10.0,
  "fwd_iat_total": 500.0,
  "fwd_iat_mean": 50.0,
  "fwd_iat_min": 5.0,
  "bwd_iat_total": 400.0,
  "bwd_iat_mean": 80.0,
  "bwd_iat_min": 8.0,
  "fwd_header_length": 200,
  "bwd_header_length": 100,
  "packet_length_max": 150.0,
  "packet_length_mean": 100.2,
  "syn_flag_count": 1,
  "ack_flag_count": 1,
  "urg_flag_count": 0,
  "down_up_ratio": 0.5,
  "active_mean": 100.0,
  "active_std": 10.0,
  "active_max": 200.0,
  "active_min": 50.0,
  "idle_mean": 50.0,
  "idle_std": 5.0,
  "idle_max": 100.0,
  "idle_min": 10.0,
  "source_ip": "192.168.1.1",
  "destination_ip": "10.0.0.1",
  "source_port": 12345,
  "destination_port": 80
}
```

#### Javob namunasi

```json
{
  "id": 1,
  "timestamp": "2023-07-01T12:34:56.789Z",
  "prediction": {
    "class": 0,
    "label": "Benign",
    "confidence": 0.95,
    "probabilities": {
      "Benign": 0.95,
      "Syn": 0.01,
      "UDP": 0.01,
      "UDPLag": 0.01,
      "LDAP": 0.005,
      "MSSQL": 0.005,
      "NetBIOS": 0.005,
      "Portmap": 0.005
    }
  },
  "data": {
    "flow_duration": 1234,
    "protocol": 6,
    "flow_bytes_s": 1000.5,
    "flow_packets_s": 10.5,
    "packet_length_mean": 100.2,
    "packet_length_std": 10.0,
    "packet_length_min": 60.0,
    "packet_length_max": 150.0,
    "source_ip": "192.168.1.1",
    "destination_ip": "10.0.0.1",
    "source_port": 12345,
    "destination_port": 80,
    "predicted_class": 0,
    "predicted_label": "Benign",
    "prediction_confidence": 0.95
  }
}
```

## Mashina o'rganish modeli

Tizim DDoS hujumlarini aniqlash va tasniflash uchun **CICDDoS2019** ma'lumotlar to'plamida o'qitilgan **Random Forest** klassifikatoridan foydalanadi. Model quyidagi hujum turlarini aniqlashi mumkin:

- **Benign**: Normal, hujumsiz trafik
- **Syn**: SYN flood hujumi
- **UDP**: Umumiy UDP flood hujumi
- **UDPLag**: Kechikish bilan UDP-asosidagi DDoS
- **LDAP**: Lightweight Directory Access Protocol-asosidagi hujum
- **MSSQL**: MSSQL-ga xos DDoS hujumi
- **NetBIOS**: NetBIOS bilan bog'liq DDoS hujumi
- **Portmap**: Portmapper-asosidagi DDoS hujumi

## Foydalanilgan texnologiyalar

### Backend
- Python
- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-SocketIO
- scikit-learn

### Frontend
- HTML/CSS/JavaScript
- Bootstrap 5
- Chart.js
- Socket.IO
- Font Awesome

### Ma'lumotlarni qayta ishlash
- pandas
- NumPy
- Matplotlib
- seaborn
