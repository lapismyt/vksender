from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
try:
	import vk_api
except ImportError:
	pass

TOKEN = "6ac24e021188a7601d9780c3e609c8c9e7fcc0dd5876f41e9b29c029b2de344732d7755a137f7d1da7958"

KV = """
BoxLayout:
	orientation: "vertical"
	valign: "top"
	TextInput:
		id: userid
		hint_text: "User ID"
		hint_size: 36
		font_size: 36
		size_hint_y: .10
	TextInput:
		id: message
		hint_text: "Message"
		size_hint_y: .10
		hint_size: 36
		font_size: 36
	Label:
		id: just
		text: ""
	Button:
		text: "START"
		size_hint_y: .10
		on_release: app.start_job(userid.text, message.text)
"""

class MainApp(App):
	
	def build(self):
		return Builder.load_string(KV)
	
	def start_job(self, user_id, message):
		try:
			vk_session = vk_api.VkApi(token = TOKEN)
			vk = vk_session.get_api()
			vk.messages.send(user_id=user_id, message=message, random_id=0)
			self.root.ids.just.text = "Done!"
		except BaseException as er:
			f = open("error.txt", "w")
			f.write(str(er))
			f.close()
			self.root.ids.just.text = "Error!"
			
	
if __name__ == "__main__":
	MainApp().run()