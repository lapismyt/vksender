from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.snackbar import Snackbar
import vk_api
import traceback
import time
vk_captcha = "" # НЕ ТРОГАТЬ!
count = 50

TOKEN = "vk1.a.02mxIV17hKvKAFTIauDgDY-ov-ULq4Ux-zoM9r1m4GpEbl4ZZQkeKP1bBtpeL8CpNEtKzPuschgEhlEda6xJmdLvoI5lp0p7teiR5MqLgbQb1p7hIcNkRh3iFvxEDqHrkuB4bttK8Ju6Nm7rKOug2nhHRLrCXA6o7GeDwg_6nG6LU6nSnRnsV_TEjlIXqh2T" # Трогать!

vk_session = vk_api.VkApi(token = TOKEN)
vk = vk_session.get_api()

KV = """
ScreenManager:
	MDScreen:
		name: "main"
		MDBoxLayout:
			orientation: "vertical"
			pos_hint: {"top": 1}
			padding: 20
			adaptive_height: True
			MDTextField:
				id: user_id
				disabled: False
				hint_text: "User ID"
				hint_size: 36
				font_size: 36
			MDBoxLayout:
				orientation: "horizontal"
				adaptive_height: True
				MDTextField:
					id: msg
					disabled: False
					hint_text: "Message"
					hint_size: 36
					font_size: 36
				MDRaisedButton:
					id: send
					disabled: False
					text: "SEND"
					font_size: 30
					pos_hint: {"right": 1}
					on_press: app.start_job(user_id.text, msg.text)
			MDBoxLayout:
				adaptive_height: True
				MDSlider:
					id: msg_count
					min: 1
					max: 100
					value: 50
					disabled: False
			MDBoxLayout:
				orientation: "horizontal"
				adaptive_height: True
				MDTextField:
					id: captcha
					hint_text: "Captcha"
					hint_size: 36
					font_size: 36
					disabled: True
				MDRaisedButton:
					id: verify
					text: "VERIFY"
					font_size: 24
					pos_hint: {"right": 1}
					disabled: True
					on_press: app.verify_captcha(user_id.text, msg.text)
			MDBoxLayout:
				orientation: "vertical"
				adaptive_height: True
				pos_hint: {"bottom": 1}
				Image:
					id: captcha_img
					source: "not_captcha.png"
"""

class MainApp(MDApp):
	def build(self):
		return Builder.load_string(KV)
		
	def on_start(self):
		self.root.current = "main"
	def start_job(self, user_id, message):
		global vk_session
		global vk
		global count
		count = round(self.root.ids.msg_count.value)
		global x
		try:
			self.root.ids.msg_count.disabled = True
			self.root.ids.send.disabled = True
			self.root.ids.msg.disabled = True
			self.root.ids.user_id.disabled = True
			for x in range(count):
				vk.messages.send(user_id=user_id, message=message, random_id=0)
				time.sleep(2)
			self.root.ids.msg_count.disabled = False
			self.root.ids.send.disabled = False
			self.root.ids.msg.disabled = False
			self.root.ids.user_id.disabled = False
			snack = Snackbar(text="Done!")
		except vk_api.exceptions.Captcha as ex:
			global vk_captcha
			vk_captcha = ex
			img = ex.get_image()
			f = open("captcha.jpg", "wb")
			f.write(img)
			f.close()
			self.root.ids.captcha_img.source = "captcha.jpg"
			self.root.ids.captcha.disabled = False
			self.root.ids.verify.disabled = False
			snack = Snackbar(text="Enter captcha, please!")
		except BaseException as err:
			f = open("error.txt", "w")
			f.write(str(err))
			f.close()
			snack = Snackbar(text="Error!\n" + str(err))
			traceback.print_exc()
		snack.open()
	def verify_captcha(self, user_id, message):
		try:
			global x
			global vk_captcha
			global count
			count = round(self.root.ids.msg_count.value)
			vk_captcha.try_again(self.root.ids.captcha.text)
			self.root.ids.captcha.disabled = True
			self.root.ids.verify.disabled = True
			self.root.ids.captcha_img.source = "not_captcha.png"
			if x < count:
				try:
					for x in range(x, count):
						vk.messages.send(user_id=user_id, message=message, random_id=0)
					self.root.ids.msg_count.disabled = False
					self.root.ids.send.disabled = False
					self.root.ids.user_id.disabled = False
					self.root.ids.msg.disabled = False
				except vk_api.exceptions.Captcha as ex:
					vk_captcha = ex
					img = ex.get_image()
					f = open("captcha.jpg", "wb")
					f.write(img)
					f.close()
					self.root.ids.captcha_img.source = "captcha.jpg"
					self.root.ids.captcha.disabled = False
					self.root.ids.verify.disabled = False
					snack = Snackbar(text="Enter captcha, please!")
			self.root.ids.verify.disabled = True
			self.root.ids.captcha.disabled = True
			self.root.ids.user_id.disabled = False
			self.root.ids.msg.disabled = False
			self.root.ids.send.disabled = False
			self.root.ids.msg_count.disabled = False
			snack = Snackbar(text="Done!")
		except BaseException as err:
			f = open("error.txt", "w")
			f.write(str(err))
			f.close()
			snack = Snackbar(text="Error!\n" + str(err))
			traceback.print_exc()
		snack.open()
		

if __name__ == "__main__":
	MainApp().run()