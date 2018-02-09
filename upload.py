#!/usr/bin/python
# coding: UTF-8

"""
FILE        :upload.py
DATE        :2017.02.23
DESCRIPTION :アップロードプログラム
NAME        :MONO WIRELESS INC.
             Hikaru Yoshida
"""

import serial
import urllib
import urllib2
import sys

# URLの指定
url = 'https://tmpsys-sangitan.appspot.com/upload'

# 動作モード
# upload: アップロード
# 指定なし: printで画面上に表示
try:
    mode = sys.argv[1]
except Exception:
    mode = "print"

# シリアルポートを開く
ser = serial.Serial('/dev/ttyUSB0',115200)

class SerialData:
    """ シリアルデータを受信し、変換する
    """

    def __init__(self):
        # 1行読み込み 末尾の改行削除
        pl = ser.readline().rstrip()
        if self.check(pl):
            self.read(pl)

    def check(self, pl):
        # 長さ
        if len(pl) != 23: return False

        # チェックサム
        lst = map(ord, pl[1:].decode('hex'))
        csum = sum(lst) & 0xff
        lst.pop()
        if csum: return False

        # データ種別
        if lst[1] != 0x81: return False

        # 全てOKなら
        return True

    def read(self, pl):
        # コマンド (0x81)
        self.command = hex(pl[1])
        # 送信元の論理デバイスID (0x78)
        self.src = hex(pl[0])
        # 送信元の個体識別番号
        self.src_long = hex(pl[5] << 24 | pl[6] << 16 | pl[7] << 8 | pl[8])
        # 宛先の論理デバイスID
        self.dst = hex(pl[9])
        # パケット識別子
        self.pktid = hex(pl[2])
        # プロトコルバージョン (0x01)
        self.prtcl_ver = hex(pl[3])
        # 受信電波品質
        self.LQI = int(pl[4])
        # タイムスタンプ
        self.time_stmp = float((pl[10] << 8 | pl[11]) / 64.0)
        # 中継フラグ
        self.relay_flg = int(pl[12])
        # 電源電圧
        self.volt = int(pl[13] << 8 | pl[14])

        # DI1..4 のデータ
        dibm = pl[16]
        dibm_chg = pl[17]
        di = {} # 現在の状態
        di_chg = {} # 一度でもLo(1)になったら1
        for i in range(1,5):
            di[i] = 0 if (dibm & 0x1) == 0 else 1
            di_chg[i] = 0 if (dibm_chg & 0x1) == 0 else 1
            dibm >>= 1
            dibm_chg >>= 1
            pass

        # 現在のデジタル入力
        self.di1_now = di[1]
        self.di2_now = di[2]
        self.di3_now = di[3]
        self.di4_now = di[4]
        # デジタル入力の変更状態
        self.di1_chg = di_chg[1]
        self.di2_chg = di_chg[2]
        self.di3_chg = di_chg[3]
        self.di4_chg = di_chg[4]

        # AD1..4 のデータ
        ad = {}
        er = pl[22]
        for i in range(1,5):
            av = pl[i + 18 - 1]
            if av == 0xFF:
                # ADポートが未使用扱い(おおむね2V以)なら -1
                ad[i] = -1
            else:
                # 補正ビットを含めた計算
                ad[i] = ((av * 4) + (er & 0x3)) * 4
            er >>= 2

        # AD値
        self.ad1 = ad[1]
        self.ad2 = ad[2]
        self.ad3 = ad[3]
        self.ad4 = ad[4]

# 読み込みループ
while True:
    try:
        sd = SerialData()
        params = urllib.urlencode({
            'devid': sd.src_long,
            'fi'   : sd.LQI,
            'bv'   : sd.volt,
            'val'  : float(sd.ad1 - 500) /10,
            'ad1'  : sd.ad1
        })
        if mode == "upload":
            urllib2.urlopen(url,params)
        else:
            print params
    except Exception:
        import traceback
        print traceback.format_exc()

ser.close()
