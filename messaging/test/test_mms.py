# -*- coding: utf-8 -*-
import datetime
import os
import unittest

from messaging.mms.message import MMSMessage

# test data extracted from heyman's
# http://github.com/heyman/mms-decoder
DATA_DIR = os.path.join(os.path.dirname(__file__), 'mms-data')

class TestMmsDecoding(unittest.TestCase):

    def test_decoding_iPhone_mms(self):
        path = os.path.join(DATA_DIR, 'iPhone.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'From': '<not inserted>', 'Transaction-Id': '1262957356-3',
            'MMS-Version': '1.2', 'To': '1337/TYPE=PLMN',
            'Message-Type': 'm-send-req',
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
        }
        smil_data = '<smil>\n<head>\n<layout>\n <root-layout/>\n<region id="Text" top="70%" left="0%" height="30%" width="100%" fit="scroll"/>\n<region id="Image" top="0%" left="0%" height="70%" width="100%" fit="meet"/>\n</layout>\n</head>\n<body>\n<par dur="10s">\n<img src="IMG_6807.jpg" region="Image"/>\n</par>\n</body>\n</smil>\n'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(len(mms.data_parts), 2)
        self.assertEqual(mms.data_parts[0].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[0].data, smil_data)
        self.assertEqual(mms.data_parts[1].content_type, 'image/jpeg')
        self.assertEqual(mms.data_parts[1].content_type_parameters,
                         {'Name': 'IMG_6807.jpg'})

    def test_decoding_SIMPLE_mms(self):
        path = os.path.join(DATA_DIR, 'SIMPLE.MMS')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'Transaction-Id': '1234', 'MMS-Version': '1.0',
            'Message-Type': 'm-retrieve-conf',
            'Date': datetime.datetime(2002, 12, 20, 22, 26, 56),
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'Simple message',
        }
        text_data = "This is a simple MMS message with a single text body part."
        self.assertEqual(mms.headers, headers)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(len(mms.data_parts), 1)
        self.assertEqual(mms.data_parts[0].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[0].data, text_data)

    def test_decoding_BTMMS_mms(self):
        path = os.path.join(DATA_DIR, 'BTMMS.MMS')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'Transaction-Id': '1234', 'MMS-Version': '1.0',
            'Message-Type': 'm-retrieve-conf',
            'Date': datetime.datetime(2003, 1, 21, 2, 57, 4),
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'BT Ignite MMS',
        }
        smil_data = '<smil><head><layout><root-layout/>\r\n<region id="Image" top="0" left="0" height="50%" width="100%" fit="hidden"/>\r\n<region id="Text" top="50%" left="0" height="50%" width="100%" fit="hidden"/>\r\n</layout>\r\n</head>\r\n<body><par dur="6825ms"><img src="btlogo.gif" region="Image"></img>\r\n<audio src="catchy_g.amr" begin="350ms" end="6350ms"></audio>\r\n</par>\r\n<par dur="3000ms"><text src="btmms.txt" region="Text"><param name="foreground-color" value="#000000"/>\r\n</text>\r\n</par>\r\n</body>\r\n</smil>\r\n\r\n'
        text_data = 'BT Ignite\r\n\r\nMMS Services'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(len(mms.data_parts), 4)
        self.assertEqual(mms.data_parts[0].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[0].data, smil_data)
        self.assertEqual(mms.data_parts[1].content_type, 'image/gif')
        self.assertEqual(mms.data_parts[2].content_type, 'audio/amr')
        self.assertEqual(mms.data_parts[3].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[3].data, text_data)

    def test_decoding_TOMSLOT_mms(self):
        path = os.path.join(DATA_DIR, 'TOMSLOT.MMS')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'From': 'allan@tomslot.com', 'Transaction-Id': '1234',
            'MMS-Version': '1.0', 'Message-Type': 'm-retrieve-conf',
            'Date': datetime.datetime(2003, 2, 16, 4, 48, 33),
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'Tom Slot Band',
        }
        smil_data = '<smil>\r\n\t<head>\r\n\t\t<meta name="title" content="smil"/>\r\n\t\t<meta name="author" content="PANASONIC"/>\r\n\t\t<layout>\r\n\t\t\t<root-layout background-color="#FFFFFF" width="132" height="176"/>\r\n\t\t\t<region id="Image" width="132" height="100" left="0" top="0" fit="meet"/>\r\n\t\t\t<region id="Text" width="132" height="34" left="0" top="100" fit="scroll"/>\r\n\t\t</layout>\r\n\t</head>\r\n\t<body>\r\n\t\t<par dur="1000ms">\r\n\t\t\t<img src="img00.jpg" region="Image"/>\r\n\t\t</par>\r\n\t\t<par dur="1000ms">\r\n\t\t\t<img src="img01.jpg" region="Image"/>\r\n\t\t</par>\r\n\t\t<par dur="1000ms">\r\n\t\t\t<img src="img02.jpg" region="Image"/>\r\n\t\t</par>\r\n\t\t<par dur="1000ms">\r\n\t\t\t<img src="img03.jpg" region="Image"/>\r\n\t\t</par>\r\n\t\t<par dur="22000ms">\r\n\t\t\t<img src="img04.jpg" region="Image"/>\r\n\t\t\t<text src="txt04.txt" region="Text">\r\n\t\t\t\t<param name="foreground-color" value="#0000F8"/>\r\n\t\t\t</text>\r\n\t\t\t<audio src="aud04.amr"/>\r\n\t\t</par>\r\n\t</body>\r\n</smil>\r\n'
        text_data = 'Presented by NowMMS\r\n'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(len(mms.data_parts), 8)
        self.assertEqual(mms.data_parts[0].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[0].data, smil_data)
        self.assertEqual(mms.data_parts[1].content_type, 'image/jpeg')
        self.assertEqual(mms.data_parts[2].content_type, 'image/jpeg')
        self.assertEqual(mms.data_parts[3].content_type, 'image/jpeg')
        self.assertEqual(mms.data_parts[4].content_type, 'image/jpeg')
        self.assertEqual(mms.data_parts[5].content_type, 'image/jpeg')
        self.assertEqual(mms.data_parts[6].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[6].data, text_data)
        self.assertEqual(mms.data_parts[7].content_type, 'audio/amr')

    def test_decoding_images_are_cut_off_debug_mms(self):
        path = os.path.join(DATA_DIR, 'images_are_cut_off_debug.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'From': '<not inserted>', 'Read-Reply': False,
            'Transaction-Id': '2112410527', 'MMS-Version': '1.0',
            'To': 'tdpt@ajajg.cdm', 'Delivery-Report': False,
            'Message-Type': 'm-send-req',
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'Picture3',
        }
        smil_data = '<smil><head><layout><root-layout height="160px" width="128px"/><region id="Top" top="0"  left="0" height="50%" width="100%" /><region id="Bottom" top="50%" left="0" height="50%" width="100%" /></layout></head><body><par dur="5s"><img src="cid:Picture3.jpg" region="Top" begin="0s" end="5s"></img></par></body></smil>'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 2)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'image/jpeg')
        self.assertEqual(mms.data_parts[0].content_type_parameters,
                         {'Name': 'Picture3.jpg'})
        self.assertEqual(mms.data_parts[1].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[1].data, smil_data)

    def test_decoding_openwave_mms(self):
        path = os.path.join(DATA_DIR, 'openwave.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'From': '+16505550000/TYPE=PLMN', 'Message-Class': 'Personal',
            'Transaction-Id': '1067263672', 'MMS-Version': '1.0',
            'Priority': 'Normal', 'To': '112/TYPE=PLMN',
            'Delivery-Report': False, 'Message-Type': 'm-send-req',
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'rubrik',
        }
        smil_data = '<smil>\n  <head>\n    <layout>\n      <root-layout width="100%" height="100%" />\n      <region id="Text" left="0%" top="0%" width="100%" height="50%" />\n      <region id="Image" left="0%" top="50%" width="100%" height="50%" />\n    </layout>\n  </head>\n  <body>\n    <par dur="30000ms">\n      <text src="cid:text_0" region="Text" />\n    </par>\n  </body>\n</smil>\n'
        text_data = 'rubrik'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 2)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[0].data, smil_data)
        self.assertEqual(mms.data_parts[1].data, text_data)

    def test_decoding_SonyEricssonT310_R201_mms(self):
        path = os.path.join(DATA_DIR, 'SonyEricssonT310-R201.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'Sender-Visibility': 'Show', 'From': '<not inserted>',
            'Read-Reply': False, 'Message-Class': 'Personal',
            'Transaction-Id': '1-8db', 'MMS-Version': '1.0',
            'Priority': 'Normal', 'To': '55225/TYPE=PLMN',
            'Delivery-Report': False, 'Message-Type': 'm-send-req',
            'Date': datetime.datetime(2004, 3, 18, 8, 30, 34),
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
        }
        text_data = 'Hej hopp'
        smil_data = '<smil><head><layout><root-layout height="240px" width="160px"/>\r\n<region id="Image" top="0" left="0" height="50%" width="100%" fit="hidden"/>\r\n<region id="Text" top="50%" left="0" height="50%" width="100%" fit="hidden"/>\r\n</layout>\r\n</head>\r\n<body><par dur="2000ms"><img src="Tony.gif" region="Image"></img>\r\n<text src="mms.txt" region="Text"></text>\r\n<audio src="OldhPhone.mid"></audio>\r\n</par>\r\n</body>\r\n</smil>\r\n'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 4)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'image/gif')
        self.assertEqual(mms.data_parts[0].content_type_parameters,
                         {'Name': 'Tony.gif'})
        self.assertEqual(mms.data_parts[1].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[1].data, text_data)
        self.assertEqual(mms.data_parts[2].content_type, 'audio/midi')
        self.assertEqual(mms.data_parts[2].content_type_parameters,
                         {'Name': 'OldhPhone.mid'})
        self.assertEqual(mms.data_parts[3].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[3].data, smil_data)

    def test_decoding_gallery2test_mms(self):
        path = os.path.join(DATA_DIR, 'gallery2test.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'From': '+16505550000/TYPE=PLMN', 'Message-Class': 'Personal',
            'Transaction-Id': '1118775337', 'MMS-Version': '1.0',
            'Priority': 'Normal', 'To': 'Jg', 'Delivery-Report': False,
            'Message-Type': 'm-send-req',
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'Jgj',
        }
        text_data = 'Jgj'
        smil_data = '<smil>\n  <head>\n    <layout>\n      <root-layout width="100%" height="100%" />\n      <region id="Text" left="0%" top="0%" width="100%" height="50%" />\n      <region id="Image" left="0%" top="50%" width="100%" height="50%" />\n    </layout>\n  </head>\n  <body>\n    <par dur="30000ms">\n      <img src="cid:image_0" region="Image" alt="gnu-head" />\n      <text src="cid:text_0" region="Text" />\n    </par>\n  </body>\n</smil>\n'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 3)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[0].data, smil_data)
        self.assertEqual(mms.data_parts[1].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[1].data, text_data)
        self.assertEqual(mms.data_parts[2].content_type, 'image/jpeg')
        # XXX: Shouldn't it be 'Name' instead ?
        self.assertEqual(mms.data_parts[2].content_type_parameters,
                         {'name': 'gnu-head.jpg'})

    def test_decoding_projekt_exempel_mms(self):
        path = os.path.join(DATA_DIR, 'projekt_exempel.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'Sender-Visibility': 'Show', 'From': '<not inserted>',
            'Read-Reply': False, 'Message-Class': 'Personal',
            'Transaction-Id': '4-fc60', 'MMS-Version': '1.0',
            'Priority': 'Normal', 'To': '12345/TYPE=PLMN',
            'Delivery-Report': False, 'Message-Type': 'm-send-req',
            'Date': datetime.datetime(2004, 5, 23, 17, 13, 40),
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'Hej',
        }
        smil_data = '<smil><head><layout><root-layout height="240px" width="160px"/>\r\n<region id="Image" top="0" left="0" height="50%" width="100%" fit="hidden"/>\r\n<region id="Text" top="50%" left="0" height="50%" width="100%" fit="hidden"/>\r\n</layout>\r\n</head>\r\n<body><par dur="2000ms"><text src="mms.txt" region="Text"></text>\r\n<img src="SonyhEr.gif" region="Image"></img>\r\n</par>\r\n</body>\r\n</smil>\r\n'
        text_data = 'Jonatan \xc3\xa4r en GNU'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 3)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[0].data, text_data)
        self.assertEqual(mms.data_parts[1].content_type, 'image/gif')
        self.assertEqual(mms.data_parts[2].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[2].data, smil_data)
        self.assertEqual(mms.data_parts[2].content_type_parameters,
                         {'Charset': 'utf-8', 'Name': 'mms.smil'})

    def test_decoding_m_mms(self):
        path = os.path.join(DATA_DIR, 'm.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'From': 'goldpost@hotmail.com', 'Transaction-Id': '0000000001',
            'MMS-Version': '1.0', 'Message-Type': 'm-retrieve-conf',
            'Date': datetime.datetime(2002, 8, 9, 15, 8, 2),
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'GOLD',
        }
        text_data1 = 'Audio'
        text_data2 = 'Text +'
        text_data3 = 'tagtag.com/gold\r\n'
        text_data4 = 'globalisierunglobalisierunglobalisierunglobalisierunglobalisierunglobalisierunglobalisierungnureisilabolg'
        text_data5 = 'KLONE\r\nKLONE\r\n'
        text_data6 = 'pr\xe4sentiert..'
        text_data7 = 'GOLD'
        smil_data = '<smil><head><layout><root-layout background-color="#000000"/>\r\n<region id="text" top="0" left="0" height="100%" width="100%"/>\r\n</layout>\r\n</head>\r\n<body>\r\n<par dur="3000ms">\r\n<text src="Text0000.txt" region="text">\r\n <param name="foreground-color" value="#ffff00"/>\r\n <param name="textsize" value="large"/>\r\n</text>\r\n</par>\r\n<par dur="2000ms">\r\n<text src="Text0001.txt" region="text">\r\n <param name="foreground-color" value="#ffff00"/>\r\n <param name="textsize" value="small"/>\r\n</text>\r\n</par>\r\n<par dur="2000ms">\r\n<text src="Text0007.txt" region="text">\r\n <param name="foreground-color" value="#ffff00"/>\r\n <param name="textsize" value="normal"/>\r\n</text>\r\n</par>\r\n<par dur="6000ms">\r\n<text src="Text0008.txt" region="text">\r\n <param name="foreground-color" value="#ffff00"/>\r\n <param name="textsize" value="normal"/>\r\n</text>\r\n<audio src="gold102.amr" start="1000ms"/>\r\n</par>\r\n<seq repeatcount="4">\r\n<par dur="1500ms">\r\n<text src="Text0002.txt" region="text">\r\n <param name="foreground-color" value="#ff0080"/>\r\n <param name="textsize" value="normal"/>\r\n</text>\r\n</par>\r\n<par dur="1500ms">\r\n<text src="Text0003.txt" region="text">\r\n <param name="foreground-color" value="#00ff00"/>\r\n <param name="textsize" value="normal"/>\r\n</text>\r\n</par>\r\n</seq>\r\n<par dur="10000ms">\r\n<text src="Text0006.txt" region="text">\r\n <param name="foreground-color" value="#ffff00"/>\r\n <param name="textsize" value="normal"/>\r\n</text>\r\n</par>\r\n</body></smil>'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 9)
        self.assertEqual(mms.content_type, 'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[0].data, text_data1)
        self.assertEqual(mms.data_parts[0].content_type_parameters,
                         {'Charset': 'us-ascii'})
        self.assertEqual(mms.data_parts[1].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[1].data, smil_data)
        self.assertEqual(mms.data_parts[1].content_type_parameters,
                         {'Charset': 'us-ascii'})
        self.assertEqual(mms.data_parts[2].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[2].data, text_data2)
        self.assertEqual(mms.data_parts[2].content_type_parameters,
                         {'Charset': 'us-ascii'})
        self.assertEqual(mms.data_parts[3].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[3].data, text_data3)
        self.assertEqual(mms.data_parts[3].content_type_parameters,
                         {'Charset': 'us-ascii'})
        self.assertEqual(mms.data_parts[4].content_type, 'audio/amr')
        self.assertEqual(mms.data_parts[5].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[5].data, text_data4)
        self.assertEqual(mms.data_parts[5].content_type_parameters,
                         {'Charset': 'us-ascii'})
        self.assertEqual(mms.data_parts[6].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[6].data, text_data5)
        self.assertEqual(mms.data_parts[6].content_type_parameters,
                         {'Charset': 'us-ascii'})
        self.assertEqual(mms.data_parts[7].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[7].data, text_data6)
        self.assertEqual(mms.data_parts[7].content_type_parameters,
                         {'Charset': 'us-ascii'})
        self.assertEqual(mms.data_parts[8].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[8].data, text_data7)
        self.assertEqual(mms.data_parts[8].content_type_parameters,
                         {'Charset': 'us-ascii'})

    def test_decoding_27d0a048cd79555de05283a22372b0eb_mms(self):
        path = os.path.join(DATA_DIR, '27d0a048cd79555de05283a22372b0eb.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'Sender-Visibility': 'Show', 'From': '<not inserted>',
            'Read-Reply': False, 'Message-Class': 'Personal',
            'Transaction-Id': '3-31cb', 'MMS-Version': '1.0',
            'Priority': 'Normal', 'To': '123/TYPE=PLMN',
            'Delivery-Report': False, 'Message-Type': 'm-send-req',
            'Date': datetime.datetime(2004, 5, 23, 16, 14, 58),
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
            'Subject': 'Angående art-tillhörighet',
            #'Subject': 'Ang\xc3\xa5ende art-tillh\xc3\xb6righet',
        }
        smil_data = '<smil><head><layout><root-layout height="240px" width="160px"/>\r\n<region id="Image" top="0" left="0" height="50%" width="100%" fit="hidden"/>\r\n<region id="Text" top="50%" left="0" height="50%" width="100%" fit="hidden"/>\r\n</layout>\r\n</head>\r\n<body><par dur="2000ms"><img src="Rain.wbmp" region="Image"></img>\r\n<text src="mms.txt" region="Text"></text>\r\n</par>\r\n</body>\r\n</smil>\r\n'
        text_data = 'Jonatan \xc3\xa4r en gnu.'
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 3)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'image/vnd.wap.wbmp')
        self.assertEqual(mms.data_parts[0].content_type_parameters,
                        {'Name': 'Rain.wbmp'})
        self.assertEqual(mms.data_parts[1].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[1].data, text_data)
        self.assertEqual(mms.data_parts[1].content_type_parameters,
                         {'Charset': 'utf-8', 'Name': 'mms.txt'})
        self.assertEqual(mms.data_parts[2].content_type, 'application/smil')
        self.assertEqual(mms.data_parts[2].data, smil_data)
        self.assertEqual(mms.data_parts[2].content_type_parameters,
                         {'Charset': 'utf-8', 'Name': 'mms.smil'})

    def test_decoding_SEC_SGHS300M(self):
        path = os.path.join(DATA_DIR, 'SEC-SGHS300M.mms')
        mms = MMSMessage.from_file(path)
        self.assertTrue(isinstance(mms, MMSMessage))
        headers = {
            'Sender-Visibility': 'Show', 'From': '<not inserted>',
            'Read-Reply': False, 'Message-Class': 'Personal',
            'Transaction-Id': '31887', 'MMS-Version': '1.0',
            'To': '0738345664/TYPE=PLMN', 'Delivery-Report': False,
            'Message-Type': 'm-send-req', 'Subject': 'IL',
            'Content-Type': ('application/vnd.wap.multipart.mixed', {}),
        }
        text_data = 'HV'
        smil_data = ''
        self.assertEqual(mms.headers, headers)
        self.assertEqual(len(mms.data_parts), 1)
        self.assertEqual(mms.content_type,
                         'application/vnd.wap.multipart.mixed')
        self.assertEqual(mms.data_parts[0].content_type, 'text/plain')
        self.assertEqual(mms.data_parts[0].data, text_data)
        self.assertEqual(mms.data_parts[0].content_type_parameters,
                         {'Charset': 'utf-8'})