import face_recognition
import cv2
from multiprocessing import Process, Manager, cpu_count, set_start_method
import time
import numpy
import threading
import platform

# kisilerin bir sonraki id'sini alma
def next_id(anlik_id, kisi_num):
    if anlik_id == kisi_num:
        return 1
    else:
        return anlik_id + 1


# kisilerin bir önceki id'sini alma
def prev_id(anlik_id, kisi_num):
    if anlik_id == 1:
        return kisi_num
    else:
        return anlik_id - 1




def capture2(kesit_listesi_oku, Global, kisi_num):
    # videodan referans alma #0
    video_capture = cv2.VideoCapture('o_ses.mp4')

    while not Global.is_exit:
        # kesiti (frame) okuma
        if Global.buff_num != next_id(Global.read_num, kisi_num):
            # video kesitinden görüntü yakalama
            ret, frame = video_capture.read()
            kesit_listesi_oku[Global.buff_num] = frame
            Global.buff_num = next_id(Global.buff_num, kisi_num)
        else:
            time.sleep(0.01)

    # videoyu bırakma
    video_capture.release()


# islem kesitlerini kullanan birçok alt islemler
def process(kisi_id, kesit_listesi_oku, kesit_listesi_yaz, Global, kisi_num):
    bilinen_yuzler = Global.bilinen_yuzler
    bilinen_yuz_isimleri = Global.bilinen_yuz_isimleri
    while not Global.is_exit:
        # okumayı bekleme
        while Global.read_num != kisi_id or Global.read_num != prev_id(Global.buff_num, kisi_num):
            time.sleep(0.01)
        # videonun daha yumusak görünmesini saglamak icin gecikme
        time.sleep(Global.frame_delay)
        # kesit listesinden tek kesit okuma
        frame_process = kesit_listesi_oku[kisi_id]
        # bir sonraki kisinin kesitini okumayı bekleme
        Global.read_num = next_id(Global.read_num, kisi_num)
        # fotografi BGR renginden (OpenCV'nin kullandigi), RGB rengine (yüz tanimada kullanilan) donusturme
        rgb_frame = frame_process[:, :, ::-1]
        # tüm yüzleri bulma ve video kesitindeki fotograflari cozme
        yuz_konumlari = face_recognition.yuz_konumlari(rgb_frame)
        yuz_kodlamalari = face_recognition.yuz_kodlamalari(rgb_frame, yuz_konumlari)
        # video kesitlerinde her yüz icin dongu olusturma
        for (top, right, bottom, left), face_encoding in zip(yuz_konumlari, yuz_kodlamalari):
            # eger kesit bilinen yüzlerle eslesiyorsa gör
            eslesmeler = face_recognition.compare_faces(bilinen_yuzler, face_encoding)
            isim = "Bilinmeyen"
            # eger bilinen_yuzlerde eslesiyorsa sadece ilk olanı kullanma
            if True in eslesmeler:
                ilk_eslesme_index = eslesmeler.index(True)
                isim = bilinen_yuz_isimleri[ilk_eslesme_index]
            # yuzun etrafına kutu cizme
            cv2.rectangle(frame_process, (left, top), (right, bottom), (0, 0, 255), 2)
            # cizilen kutunun altina isim yazma
            cv2.rectangle(frame_process, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame_process, isim, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # yazmayi bekleme
        while Global.write_num != kisi_id:
            time.sleep(0.01)
        # global e kesit gönderme
        kesit_listesi_yaz[kisi_id] = frame_process
        # kesit yazma icin yeni kisiyi bekleme
        Global.write_num = next_id(Global.write_num, kisi_num)


if __name__ == '__main__':

    #MacOS'ta Fix Bug
    if platform.system() == 'Darwin':
        set_start_method('forkserver')

    # Global degerler
    Global = Manager().Namespace()
    Global.buff_num = 1
    Global.read_num = 1
    Global.write_num = 1
    Global.frame_delay = 0
    Global.is_exit = False
    kesit_listesi_oku = Manager().dict()
    kesit_listesi_yaz = Manager().dict()

    # kisilerin sayisi(kesitleri islemek icin alt islem)
    if cpu_count() > 8:
        kisi_num = cpu_count() - 1  # 1 tutulan kesitler icin
    else:
        kisi_num = 8

    # alt islem listesi
    p = []

    # kesitleri tutmak icin thread olusturma (eger alt islem kullanıyorsa, Mac'te crash olacak)
    p.append(threading.Thread(target=capture2, args=(kesit_listesi_oku, Global, kisi_num,)))
    p[0].start()
    
    
    # ornek resim yukleyip tanimlama
    hadise_fotograf = face_recognition.load_image_file("hadise.jpg")
    hadise_yuz_kodlama = face_recognition.yuz_kodlamalari(hadise_fotograf)[0]
    
     # ornek resim yukleyip tanimlama
    hadise1_fotograf = face_recognition.load_image_file("hadise1.jpg")
    hadise1_yuz_kodlama = face_recognition.yuz_kodlamalari(hadise1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    hadise2_fotograf = face_recognition.load_image_file("hadise2.jpg")
    hadise2_yuz_kodlama = face_recognition.yuz_kodlamalari(hadise2_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    hadise3_fotograf = face_recognition.load_image_file("hadise3.jpg")
    hadise3_yuz_kodlama = face_recognition.yuz_kodlamalari(hadise3_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    hadise4_fotograf = face_recognition.load_image_file("hadise4.jpg")
    hadise4_yuz_kodlama = face_recognition.yuz_kodlamalari(hadise4_fotograf)[0]
    
    
    
    # ornek resim yukleyip tanimlama
    beyaz_fotograf = face_recognition.load_image_file("beyaz.jpg")
    beyaz_yuz_kodlama = face_recognition.yuz_kodlamalari(beyaz_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    beyaz1_fotograf = face_recognition.load_image_file("beyaz1.jpg")
    beyaz1_yuz_kodlama = face_recognition.yuz_kodlamalari(beyaz1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    beyaz2_fotograf = face_recognition.load_image_file("beyaz2.jpg")
    beyaz2_yuz_kodlama = face_recognition.yuz_kodlamalari(beyaz2_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    beyaz3_fotograf = face_recognition.load_image_file("beyaz3.jpg")
    beyaz3_yuz_kodlama = face_recognition.yuz_kodlamalari(beyaz3_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    beyaz4_fotograf = face_recognition.load_image_file("beyaz4.jpg")
    beyaz4_yuz_kodlama = face_recognition.yuz_kodlamalari(beyaz4_fotograf)[0]
    
    

    # ornek resim yukleyip tanimlama
    murat_fotograf = face_recognition.load_image_file("murat.jpg")
    murat_yuz_kodlama = face_recognition.yuz_kodlamalari(murat_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    murat1_fotograf = face_recognition.load_image_file("murat1.jpg")
    murat1_yuz_kodlama = face_recognition.yuz_kodlamalari(murat1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    murat2_fotograf = face_recognition.load_image_file("murat2.jpg")
    murat2_yuz_kodlama = face_recognition.yuz_kodlamalari(murat2_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    murat3_fotograf = face_recognition.load_image_file("murat3.jpg")
    murat3_yuz_kodlama = face_recognition.yuz_kodlamalari(murat3_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    murat4_fotograf = face_recognition.load_image_file("murat4.jpg")
    murat4_yuz_kodlama = face_recognition.yuz_kodlamalari(murat4_fotograf)[0]
    
    
    
    # ornek resim yukleyip tanimlama
    acun_fotograf = face_recognition.load_image_file("acun.jpg")
    acun_yuz_kodlama = face_recognition.yuz_kodlamalari(acun_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    acun1_fotograf = face_recognition.load_image_file("acun1.jpg")
    acun1_yuz_kodlama = face_recognition.yuz_kodlamalari(acun1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    acun2_fotograf = face_recognition.load_image_file("acun2.jpg")
    acun2_yuz_kodlama = face_recognition.yuz_kodlamalari(acun2_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    acun3_fotograf = face_recognition.load_image_file("acun3.jpg")
    acun3_yuz_kodlama = face_recognition.yuz_kodlamalari(acun3_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    acun4_fotograf = face_recognition.load_image_file("acun4.jpg")
    acun4_yuz_kodlama = face_recognition.yuz_kodlamalari(acun4_fotograf)[0]

    
    
    # ornek resim yukleyip tanimlama
    seda_fotograf = face_recognition.load_image_file("seda.jpg")
    seda_yuz_kodlama = face_recognition.yuz_kodlamalari(seda_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    seda1_fotograf = face_recognition.load_image_file("seda1.jpg")
    seda1_yuz_kodlama = face_recognition.yuz_kodlamalari(seda1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    seda2_fotograf = face_recognition.load_image_file("seda2.jpg")
    seda2_yuz_kodlama = face_recognition.yuz_kodlamalari(seda2_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    seda3_fotograf = face_recognition.load_image_file("seda3.jpg")
    seda3_yuz_kodlama = face_recognition.yuz_kodlamalari(seda3_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    seda4_fotograf = face_recognition.load_image_file("seda4.jpg")
    seda4_yuz_kodlama = face_recognition.yuz_kodlamalari(seda4_fotograf)[0]
    
    
    
    # ornek resim yukleyip tanimlama
    asli_fotograf = face_recognition.load_image_file("asli.jpg")
    asli_yuz_kodlama = face_recognition.yuz_kodlamalari(asli_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    asli1_fotograf = face_recognition.load_image_file("asli1.jpg")
    asli1_yuz_kodlama = face_recognition.yuz_kodlamalari(asli1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    asli2_fotograf = face_recognition.load_image_file("asli2.jpg")
    asli2_yuz_kodlama = face_recognition.yuz_kodlamalari(asli2_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    asli3_fotograf = face_recognition.load_image_file("asli3.jpg")
    asli3_yuz_kodlama = face_recognition.yuz_kodlamalari(asli3_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    asli4_fotograf = face_recognition.load_image_file("asli4.jpg")
    asli4_yuz_kodlama = face_recognition.yuz_kodlamalari(asli4_fotograf)[0]
    
    
    
    # ornek resim yukleyip tanimlama
    burak_fotograf = face_recognition.load_image_file("burak.jpg")
    burak_yuz_kodlama = face_recognition.yuz_kodlamalari(burak_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    burak1_fotograf = face_recognition.load_image_file("burak1.jpg")
    burak1_yuz_kodlama = face_recognition.yuz_kodlamalari(burak1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    burak2_fotograf = face_recognition.load_image_file("burak2.jpg")
    burak2_yuz_kodlama = face_recognition.yuz_kodlamalari(burak2_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    burak3_fotograf = face_recognition.load_image_file("burak3.jpg")
    burak3_yuz_kodlama = face_recognition.yuz_kodlamalari(burak3_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    burak4_fotograf = face_recognition.load_image_file("burak4.jpg")
    burak4_yuz_kodlama = face_recognition.yuz_kodlamalari(burak4_fotograf)[0]
    
    
    
    # ornek resim yukleyip tanimlama
    fahriye_fotograf = face_recognition.load_image_file("fahriye.jpg")
    fahriye_yuz_kodlama = face_recognition.yuz_kodlamalari(fahriye_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    fahriye1_fotograf = face_recognition.load_image_file("fahriye1.jpg")
    fahriye1_yuz_kodlama = face_recognition.yuz_kodlamalari(fahriye1_fotograf)[0]
    
    # ornek resim yukleyip tanimlama
    fahriye2_fotograf = face_recognition.load_image_file("fahriye2.jpg")
    fahriye2_yuz_kodlama = face_recognition.yuz_kodlamalari(fahriye2_fotograf)[0]
    
     # ornek resim yukleyip tanimlama
    fahriye3_fotograf = face_recognition.load_image_file("fahriye3.jpg")
    fahriye3_yuz_kodlama = face_recognition.yuz_kodlamalari(fahriye3_fotograf)[0]
    
     # ornek resim yukleyip tanimlama
    fahriye4_fotograf = face_recognition.load_image_file("fahriye4.jpg")
    fahriye4_yuz_kodlama = face_recognition.yuz_kodlamalari(fahriye4_fotograf)[0]


    # bilinen yuz kodlamalari ve isimleriyle dizi olusturma
    Global.bilinen_yuzler = [
        hadise_yuz_kodlama,
        hadise1_yuz_kodlama,
        hadise2_yuz_kodlama,
        hadise3_yuz_kodlama,
        hadise4_yuz_kodlama,
        beyaz_yuz_kodlama,
        beyaz1_yuz_kodlama,
        beyaz2_yuz_kodlama,
        beyaz3_yuz_kodlama,
        beyaz4_yuz_kodlama,
        murat_yuz_kodlama,
        murat1_yuz_kodlama,
        murat2_yuz_kodlama,
        murat3_yuz_kodlama,
        murat4_yuz_kodlama,
        acun_yuz_kodlama,
        acun1_yuz_kodlama,
        acun2_yuz_kodlama,
        acun3_yuz_kodlama,
        acun4_yuz_kodlama,
        seda_yuz_kodlama,
        seda1_yuz_kodlama,
        seda2_yuz_kodlama,
        seda3_yuz_kodlama,
        seda4_yuz_kodlama,
        asli_yuz_kodlama,
        asli1_yuz_kodlama,
        asli2_yuz_kodlama,
        asli3_yuz_kodlama,
        asli4_yuz_kodlama,
        burak_yuz_kodlama,
        burak1_yuz_kodlama,
        burak2_yuz_kodlama,
        burak3_yuz_kodlama,
        burak4_yuz_kodlama,
        fahriye_yuz_kodlama,
        fahriye1_yuz_kodlama,
        fahriye2_yuz_kodlama,
        fahriye3_yuz_kodlama,
        fahriye4_yuz_kodlama
    ]
    Global.bilinen_yuz_isimleri = [
        "Hadise",
        "Hadise",
        "Hadise",
        "Hadise",
        "Hadise",
        "Beyaz",
        "Beyaz",
        "Beyaz",
        "Beyaz",
        "Beyaz",
        "Murat",
        "Murat",
        "Murat",
        "Murat",
        "Murat",
        "Acun",
        "Acun",
        "Acun",
        "Acun",
        "Acun",
        "Seda",
        "Seda",
        "Seda",
        "Seda",
        "Seda",
        "Asli",
        "Asli",
        "Asli",
        "Asli",
        "Asli",
        "Burak",
        "Burak",
        "Burak",
        "Burak",
        "Burak",
        "Fahriye",
        "Fahriye",
        "Fahriye",
        "Fahriye",
        "Fahriye"
    ]

    # kisileri olusturma
    for kisi_id in range(1, kisi_num + 1):
        p.append(Process(target=process, args=(kisi_id, kesit_listesi_oku, kesit_listesi_yaz, Global, kisi_num,)))
        p[kisi_id].start()

    # videoyu gostermeye baslama
    last_num = 1
    fps_list = []
    tmp_time = time.time()
    while not Global.is_exit:
        while Global.write_num != last_num:
            last_num = int(Global.write_num)

            # fps'i hesaplama
            delay = time.time() - tmp_time
            tmp_time = time.time()
            fps_list.append(delay)
            if len(fps_list) > 5 * kisi_num:
                fps_list.pop(0)
            fps = len(fps_list) / numpy.sum(fps_list)
            print("fps: %.2f" % fps)

            # videoyu daha yumusak yapmak yerine kesit gecikmesini hesaplama
            # eger fps daha yuksekse, daha kucuk oran (ratio) kullanilmali, veya fps daha dusuk degerle sinirlanacaktir
            # daha uzun oran videoyu daha yumusak yapar, fakat fps daha yuksek olmak icin zorlar
            # daha kucuk oran fps'i daha yuksek yapar fakat video cok yumusak gorunmez
            # bircok kez test edilen oranlar asagida
            if fps < 6:
                Global.frame_delay = (1 / fps) * 0.75
            elif fps < 20:
                Global.frame_delay = (1 / fps) * 0.5
            elif fps < 30:
                Global.frame_delay = (1 / fps) * 0.25
            else:
                Global.frame_delay = 0

            # sonuc fotografini gosterme
            cv2.imshow('Video', kesit_listesi_yaz[prev_id(Global.write_num, kisi_num)])

        # cikmak icin kalvyenin 'q' tusuna basma
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Global.is_exit = True
            break

        time.sleep(0.01)

    # cikis
    cv2.destroyAllWindows()