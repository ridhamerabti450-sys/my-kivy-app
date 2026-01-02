from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.uix.image import Image
import math

KV = '''
BoxLayout:
    orientation: 'vertical'

    # Header bar
    BoxLayout:
        size_hint_y: None
        height: dp(70)
        padding: dp(10)
        spacing: dp(15)
        canvas.before:
            Color:
                rgba: 0x47/255.0, 0x0B/255.0, 0x00/255.0, 1
            Rectangle:
                pos: self.pos
                size: self.size

        # استخدام الكلاس المخصص للشعار ليدور عند اللمس فقط
        AnimatedLogo:
            id: logo_img
            source: 'logo.png'
            size_hint: None, None
            size: dp(67), dp(67)
            allow_stretch: True
            keep_ratio: True
            pos_hint: {'center_y': 0.5}
            canvas.before:
                PushMatrix
                Rotate:
                    angle: self.angle
                    origin: self.center
            canvas.after:
                PopMatrix

        Label:
            text: 'DST Analyzer'
            font_size: dp(24)
            bold: True
            color: 1, 1, 1, 1
            halign: 'left'
            valign: 'middle'
            text_size: self.size

    TabbedPanel:
        do_default_tab: False
        tab_pos: 'top_mid'
        tab_width: self.width / 3
        tab_height: dp(48)

        TabbedPanelItem:
            text: 'Copper'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(12)
                spacing: dp(8)

                ScrollView:
                    do_scroll_x: False
                    do_scroll_y: True

                    GridLayout:
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(8)

                        Label:
                            text: 'Advanced Copper Analysis'
                            size_hint_y: None
                            height: dp(30)

                        GridLayout:
                            cols: 2
                            size_hint_y: None
                            height: self.minimum_height
                            row_default_height: dp(40)
                            row_force_default: False
                            spacing: dp(6)
                            padding: dp(4)

                            Label:
                                text: 'Cable Category:'
                            Spinner:
                                id: c_cat
                                text: 'Select Cable Category'
                                values: app.copper_categories
                                background_normal: ''
                                background_color: [0x47/255.0, 0x0B/255.0, 0x00/255.0, 1]
                                on_text: app.on_spinner_select(self)

                            Label:
                                text: 'Data Rate:'
                            Spinner:
                                id: c_rate
                                text: 'Select Data Rate'
                                values: app.speed_keys
                                background_normal: ''
                                background_color: [0x47/255.0, 0x0B/255.0, 0x00/255.0, 1]
                                on_text: app.on_spinner_select(self)

                            Label:
                                text: 'Horizontal Length (m):'
                            TextInput:
                                id: c_hlen
                                text: '90'
                                input_filter: 'float'

                            Label:
                                text: 'Patch Cords (m):'
                            TextInput:
                                id: c_plen
                                text: '5'
                                input_filter: 'float'

                            Label:
                                text: 'Temperature (°C):'
                            TextInput:
                                id: c_temp
                                text: '20'
                                input_filter: 'float'

                            Label:
                                text: 'Frequency (MHz):'
                            TextInput:
                                id: c_freq
                                text: '100'
                                input_filter: 'float'

                        BoxLayout:
                            size_hint_y: None
                            height: dp(56)
                            padding: dp(6)
                            Button:
                                text: 'Test Copper Link'
                                on_release: app.calculate_copper()

                        Label:
                            id: c_status
                            text: ''
                            size_hint_y: None
                            height: dp(30)
                            color: app.status_color

                        TextInput:
                            id: c_report
                            text: ''
                            size_hint_y: None
                            height: dp(180)
                            readonly: True
                            multiline: True
                            font_size: dp(14)
                            background_color: 1,1,1,1

        TabbedPanelItem:
            text: 'Fiber'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(12)
                spacing: dp(8)

                ScrollView:
                    do_scroll_x: False
                    do_scroll_y: True

                    GridLayout:
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(8)

                        Label:
                            text: 'Advanced Fiber Analysis'
                            size_hint_y: None
                            height: dp(30)

                        GridLayout:
                            cols: 2
                            size_hint_y: None
                            height: self.minimum_height
                            row_default_height: dp(40)
                            row_force_default: False
                            spacing: dp(6)
                            padding: dp(4)

                            Label:
                                text: 'Fiber Type:'
                            Spinner:
                                id: f_type
                                text: 'Select Fiber Type'
                                values: app.fiber_types
                                background_normal: ''
                                background_color: [0x47/255.0, 0x0B/255.0, 0x00/255.0, 1]
                                on_text: app.on_spinner_select(self)

                            Label:
                                text: 'Distance (km):'
                            TextInput:
                                id: f_dist
                                text: '5'
                                input_filter: 'float'

                            Label:
                                text: 'Connectors:'
                            TextInput:
                                id: f_conns
                                text: '2'
                                input_filter: 'int'

                            Label:
                                text: 'Splices:'
                            TextInput:
                                id: f_splices
                                text: '0'
                                input_filter: 'int'

                            Label:
                                text: 'Data Rate:'
                            Spinner:
                                id: f_rate
                                text: 'Select Data Rate'
                                values: app.fiber_speed_keys
                                background_normal: ''
                                background_color: [0x47/255.0, 0x0B/255.0, 0x00/255.0, 1]
                                on_text: app.on_spinner_select(self)

                        BoxLayout:
                            size_hint_y: None
                            height: dp(56)
                            padding: dp(6)
                            Button:
                                text: 'Test Fiber Link'
                                on_release: app.calculate_fiber()

                        Label:
                            id: f_status
                            text: ''
                            size_hint_y: None
                            height: dp(30)
                            color: app.status_color

                        TextInput:
                            id: f_report
                            text: ''
                            size_hint_y: None
                            height: dp(160)
                            readonly: True
                            multiline: True
                            font_size: dp(14)
                            background_color: 1,1,1,1

        TabbedPanelItem:
            text: 'Standards & Info'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(12)
                Label:
                    text: app.root_info
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]
'''

# تعريف الكلاس المخصص للشعار للتعامل مع اللمس والدوران
class AnimatedLogo(Image):
    angle = NumericProperty(0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # تدوير الشعار 360 درجة عند لمسه
            # قمنا بزيادة الزاوية الحالية بمقدار 360 درجة ليدور مرة كاملة في كل لمسة
            anim = Animation(angle=self.angle + 360, duration=0.85, t='in_out_quad')
            anim.start(self)
            return True
        return super().on_touch_down(touch)

class NetworkAnalyzerApp(App):
    root_info = StringProperty("[ STANDARDS ]\n- Cat6a: 10Gbps @ 100m\n- Cat6: 10Gbps @ 55m\n- Cat8: 40Gbps @ 30m\n- Fiber Safety: 3.0dB Margin")
    status_color = ListProperty([1, 1, 1, 1])
    selected_bg_color = ListProperty([0x47/255.0, 0x0B/255.0, 0x00/255.0, 1])

    def build(self):
        self.standards = {
            "Cat5":  {"max_speed": 0.1,  "max_freq": 100,  "limit": 100, "a": 1.967, "b": 0.023, "c": 0.050},
            "Cat5e": {"max_speed": 1.0,  "max_freq": 100,  "limit": 100, "a": 1.850, "b": 0.020, "c": 0.040},
            "Cat6":  {"max_speed": 10.0, "max_freq": 250,  "limit": 100, "a": 1.808, "b": 0.017, "c": 0.100},
            "Cat6a": {"max_speed": 10.0, "max_freq": 500,  "limit": 100, "a": 1.536, "b": 0.009, "c": 0.150},
            "Cat7":  {"max_speed": 10.0, "max_freq": 600,  "limit": 100, "a": 1.500, "b": 0.008, "c": 0.120},
            "Cat8":  {"max_speed": 40.0, "max_freq": 2000, "limit": 30,  "a": 1.350, "b": 0.007, "c": 0.100}
        }
        self.speed_map = {
            "2 Mbps": 0.002, "10 Mbps": 0.01, "100 Mbps": 0.1,
            "1000 Mbps": 1.0, "10 Gbps": 10.0, "40 Gbps": 40.0
        }
        self.fiber_db = {
            "SM G.652 (1310nm)": {"loss": 0.35, "budget": 20},
            "SM G.652 (1550nm)": {"loss": 0.22, "budget": 22},
            "MM OM1 (850nm)": {"loss": 3.50, "budget": 10},
            "MM OM2 (850nm)": {"loss": 2.90, "budget": 12},
            "MM OM3 (850nm)": {"loss": 2.50, "budget": 15},
            "MM OM4 (850nm)": {"loss": 2.30, "budget": 16},
            "MM OM5 (850nm)": {"loss": 2.20, "budget": 17}
        }
        self.f_speeds = {"1 Gbps": 2, "10 Gbps": 5, "40 Gbps": 8, "100 Gbps": 11}

        self.copper_categories = list(self.standards.keys())
        self.speed_keys = list(self.speed_map.keys())
        self.fiber_types = list(self.fiber_db.keys())
        self.fiber_speed_keys = list(self.f_speeds.keys())

        return Builder.load_string(KV)
    def on_start(self):
        logo = self.root.ids.logo_img
        # أنيميشن النبض: تكبير ثم تصغير مستمر
        pulse = Animation(size=(dp(75), dp(75)), duration=0.8, t='in_out_quad')
        pulse += Animation(size=(dp(67), dp(67)), duration=0.8, t='in_out_quad')
       
        final_anim = pulse
        final_anim.start(logo)

    def popup_error(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(0.85, 0.4)).open()

    def on_spinner_select(self, spinner):
        try:
            spinner.background_color = self.selected_bg_color
            spinner.color = (1, 1, 1, 1) 
        except Exception:
            pass

    def calculate_copper(self):
        root = self.root
        try:
            cat = root.ids.c_cat.text
            speed_str = root.ids.c_rate.text
            if cat == 'Select Cable Type' or speed_str == 'Select Data Rate':
                self.popup_error("Input Error", "Please select cable category and data rate.")
                return
            
            req_speed = self.speed_map.get(speed_str)
            h_len = float(root.ids.c_hlen.text or 0)
            p_len = float(root.ids.c_plen.text or 0)
            temp = float(root.ids.c_temp.text or 20)
            freq = float(root.ids.c_freq.text or 100)

            total_len = h_len + p_len
            std = self.standards[cat]
            status = "PASS"
            color = [0, 0.6, 0, 1]
            reasons = []

            if req_speed > std["max_speed"]:
                status = "FAIL"
                color = [0.78, 0.12, 0.21, 1]
                reasons.append(f"[X] {cat} NOT standard for {speed_str}")

            if total_len > std["limit"]:
                status = "FAIL"
                color = [0.78, 0.12, 0.21, 1]
                reasons.append(f"[X] Length {total_len:.1f} m exceeds limit ({std['limit']} m)")

            alpha = (std['a'] * math.sqrt(freq) + std['b'] * freq + std['c'] / math.sqrt(freq))
            loss = (total_len / 100.0) * alpha
            if temp > 20:
                loss *= (1 + (temp - 20) * 0.004)

            report = f"Report for {speed_str} on {cat}:\n"
            report += f"• Total length: {total_len:.2f} m\n"
            report += f"• Attenuation: {loss:.2f} dB\n\n"
            report += "\n".join(reasons) if reasons else "[OK] Link is within standards."

            root.ids.c_status.text = status
            self.status_color = color
            root.ids.c_report.text = report

        except Exception as e:
            self.popup_error("Error", f"Check inputs. Error: {e}")

    def calculate_fiber(self):
        root = self.root
        try:
            f_type = root.ids.f_type.text
            speed = root.ids.f_rate.text

            if f_type == 'Select Fiber Type' or speed == 'Select Data Rate':
                self.popup_error("Input Error", "Please select fiber type and data rate.")
                return

            dist = float(root.ids.f_dist.text or 0)
            conns = int(root.ids.f_conns.text or 0)
            splices = int(root.ids.f_splices.text or 0)

            f_data = self.fiber_db.get(f_type)
            net_loss = (dist * f_data['loss']) + (conns * 0.75) + (splices * 0.1)
            max_budget = f_data['budget'] - self.f_speeds.get(speed, 0)
            headroom = max_budget - (net_loss + 3.0)

            status = "PASS" if headroom > 0 else "FAIL"
            color = [0, 0.6, 0, 1] if headroom > 0 else [0.78, 0.12, 0.21, 1]
            
            report = f"Fiber Type: {f_type}\n"
            report += f"• Distance: {dist:.2f} km\n"
            report += f"• Net Loss: {net_loss:.2f} dB\n"
            report += f"• Headroom (after 3 dB safety): {headroom:.2f} dB"

            root.ids.f_status.text = status
            self.status_color = color
            root.ids.f_report.text = report

        except Exception as e:
            self.popup_error("Error", f"Check inputs. Error: {e}")

if __name__ == '__main__':
    NetworkAnalyzerApp().run()
