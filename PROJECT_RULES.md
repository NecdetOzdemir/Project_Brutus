Sen kıdemli bir Robotik ve Makine Öğrenmesi (Deep Reinforcement Learning) mühendisisin. Seninle ROS 2 (Humble) ve Gazebo simülasyon ortamında, diferansiyel sürüşlü bir robotun labirent içindeki bir hedefi bulması için PPO (Proximal Policy Optimization) tabanlı bir otonom navigasyon sistemi geliştireceğiz.

Görevimiz: Gerekli ortam kurulumlarını yapmak ve Stable Baselines3 ile Gymnasium kütüphanelerini kullanarak, ROS 2 haberleşmesi ile entegre çalışan özel bir "RobotMazeEnv" ortamı (Custom Environment) oluşturmak.

Lütfen bana aşağıda belirtilen sırayla tam bir kurulum rehberi ve kod iskeleti üret:

1. ORTAM KURULUMU VE KONTROL (Bash Komutları):
Bana öncelikle sistemde ROS 2 Humble'ın kurulu olup olmadığını kontrol eden, kurulu değilse kurulum yönlendirmesi yapan bir bash scripti veya terminal komutları listesi ver. 
Ardından proje için bir Python sanal ortamı (virtual environment) oluşturma komutlarını yaz. 
ÖNEMLİ: ROS 2 paketlerinin sanal ortamda tanınması için sanal ortamı mutlaka `--system-site-packages` argümanı ile oluştur. 
Sonrasında bu sanal ortama kurulacak gerekli kütüphaneleri (gymnasium, stable-baselines3, torch, vb.) içeren bir `requirements.txt` dosyası veya `pip install` komutu sağla.

2. KÜTÜPHANELER VE MİMARİ:
- Rclpy (ROS 2 Python Client)
- Gymnasium (gymnasium.Env sınıfından miras alınacak)
- Stable Baselines3 (PPO algoritması)

3. CUSTOM ENVIRONMENT (RobotMazeEnv) ÖZELLİKLERİ:
- Observation Space (Durum Uzayı): Lidar'dan ( /scan topic'i, sensor_msgs/LaserScan ) gelen 360 derecelik mesafe ölçümleri. Tipi: `spaces.Box(low=0.0, high=10.0, shape=(360,), dtype=np.float32)`.
- Action Space (Eylem Uzayı): Modelin öğrenmesini hızlandırmak için Ayrık (Discrete) uzay seçilmiştir. 3 eylem:
  * 0: Düz git (Twist: linear.x > 0.0, angular.z = 0.0)
  * 1: Olduğun yerde Sola dön (Twist: linear.x = 0.0, angular.z > 0.0)
  * 2: Olduğun yerde Sağa dön (Twist: linear.x = 0.0, angular.z < 0.0)
  Komutlar /cmd_vel topic'ine (geometry_msgs/Twist) yayınlanmalıdır.

4. ÖDÜL VE CEZA FONKSİYONU (Reward Shaping - Başlangıç Taslağı):
- Hedefe ulaşıldığında: +100 puan (Terminal durum: done=True)
- Lidar verisinde duvara çok yaklaşıldığında (Çarpışma): -10 puan (Terminal durum: done=True)
- Adım cezası (En kısa yolu bulması için her 'step' çağrısında): -0.1 puan

5. KRİTİK MÜHENDİSLİK NOTU (Senkronizasyon):
Gymnasium'un `step()` fonksiyonu senkron (beklemeli) çalışır, ancak ROS 2 topic'leri (callback'ler) asenkrondur. Lütfen `RobotMazeEnv` sınıfı içinde Lidar verisinin gelmesini bekleyen ve ROS 2 düğümünü doğru bir şekilde spin eden (örneğin rclpy.spin_once() veya Threading kullanarak) blokajsız (non-blocking) bir haberleşme yapısı kur. Model kör (Lidar verisi boş) kalmamalıdır.

6. İSTENEN KOD ÇIKTILARI:
Lütfen kurulum adımlarından sonra bana adım adım proje yapısını, ROS 2 paket konfigürasyonunu ('setup.py', 'package.xml'), ROS 2 node'u olarak çalışacak 'robot_maze_env.py' dosyasını ve SB3 PPO modelini başlatacak 'train.py' kodunu ver. Kodların modüler olmasına ve açıklayıcı yorum satırları içermesine dikkat et.
