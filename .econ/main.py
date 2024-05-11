import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json


class ImageConfiguration:
    def __init__(self,root, user:str, file_paths:list, images_config:list):
        self.root = root
        self.index_images = 0
        self.images =[Image.open(file_path) for file_path in file_paths]
        self.images_config = images_config
        self.user = user
        self.user_data = {}
        self.root.title("Image Presentation App")
        self.root.geometry("1300x720")
        self.timer_id = None

        self.start_button = tk.Button(self.root, text="Start", command=self.start_presentation_in_loop)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(self.root,bg = "black")
        self.canvas.pack(padx=10, pady=10)
        self.wait_for_input()


    def wait_for_input(self):
        self.root.bind('<Key>', self.on_key_pressed)
        self.root.bind('<Button>', self.on_mouse_click)
    
    def on_mouse_click(self, event):
        if self.images_config[self.index_images]["mouse_click"] != False:
            if event.num == 1:
                self.next_image()
            elif event.num == 3:
                self.prev_image()

    def on_key_pressed(self, event):
        if event.char == self.images_config[self.index_images]["forward"] and self.images_config[self.index_images]["forward"] != None :
            self.next_image()
        elif event.char == self.images_config[self.index_images]["backward"] and self.images_config[self.index_images]["backward"] != None:
            self.prev_image()
        elif event.keysym == 'Right':
            self.next_image()
        elif event.keysym == 'Left':
            self.prev_image()
        elif event.keysym == 'space':
            self.index_images = 0
            self.show_images_config()
        elif event.char.isdigit():  
            if 1 <= int(event.char) <= 5: 
                self.user_data[self.index_images] = int(event.char)
                with open(r"data.json", "r") as json_file:
                    data = json.load(json_file)
                data[self.user] = self.user_data
                with open(r"data.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)


    def next_image(self):
        if self.index_images < len(self.images_config) - 1:
            self.index_images += 1
        self.show_images_config()
        self.reset_timer()
    
    def prev_image(self):
        if self.index_images > 0:
            self.index_images -= 1
        self.show_images_config()
        self.reset_timer()
        
    def start_presentation_in_loop(self):
        self.show_images_config()
        self.start_timer()

    def start_timer(self):
        if self.images_config[self.index_images]["time"] != None:
            self.timer_id = self.root.after(self.images_config[self.index_images]["time"], self.next_image)

    def reset_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id) 
            self.start_timer()
    
    def liked(self):
        self.like = True

    def show_images_config(self):

        self.canvas.delete("all")
        image = self.images[self.index_images]
        aspect_ratio = image.width / image.height
        max_canvas_width = self.root.winfo_width()
        max_canvas_height = self.root.winfo_height() # Exclude the height of the button frame
        if image.width > max_canvas_width or image.height > max_canvas_height:
            # If the image is larger than the canvas, resize it while maintaining aspect ratio
            if max_canvas_width / max_canvas_height < aspect_ratio:
                new_width = max_canvas_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_canvas_height
                new_width = int(new_height * aspect_ratio)
            image = image.resize((new_width, new_height))

        img = ImageTk.PhotoImage(image)
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img


class Configuration:
    def __init__(self, root):
        self.list_images_with_config = []
        self.current_image_index = 0
        self.images = []
        self.file_path = []

        self.root = root
        self.root.title("Image Configuration")
        self.root.geometry("500x750")
        root.configure(bg="black")
        
        self.frame_for_buttons = tk.Frame(self.root,bg= 'gray')
        self.frame_for_buttons.place(x=50, y=650, width=400, height=50)
        self.load_button = tk.Button(self.frame_for_buttons, text="Select Images", command=self.load_images)
        self.load_button.pack(side=tk.LEFT,padx=27, pady=10)
        self.prev_button = tk.Button(self.frame_for_buttons, text="<<", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=27, pady=10)
        self.next_button = tk.Button(self.frame_for_buttons, text=">>", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=27, pady=10)
        self.start_button = tk.Button(self.frame_for_buttons, text="Start", command=self.start_presentation)
        self.start_button.pack(side=tk.LEFT, padx=27, pady=10)

        
        self.img_settings = tk.Frame(self.root,bg="gray")
        self.img_settings.place(x=50, y=50, width=400)
        
        # frame for user key
        self.user = tk.Frame(self.img_settings)
        self.user.pack(padx=10, pady=5)
        self.label_user = tk.Label(self.user, text="user : ")
        self.label_user.pack(side=tk.LEFT,padx=60, pady=10)
        self.entry_user = tk.Entry(self.user)
        self.entry_user.pack(side=tk.RIGHT,padx=60, pady=10)

        # frame for time 
        self.frame_for_time = tk.Frame(self.img_settings)
        self.frame_for_time.pack(padx=10, pady=5)
        self.label_time = tk.Label(self.frame_for_time, text="Wait Time : ")
        self.label_time.pack(side=tk.LEFT,padx=30, pady=10)
        self.check_time = tk.BooleanVar(value=False)
        self.check_time_button = tk.Checkbutton(self.frame_for_time, text="True", variable=self.check_time, command=self.allow_entry)
        self.check_time_button.pack(side=tk.LEFT,padx=10, pady=10)
        self.entry_time = tk.Entry(self.frame_for_time)
        self.entry_time.pack(side=tk.LEFT,padx=10, pady=10)
        self.entry_time.config(state=tk.DISABLED)
        self.label_time_ = tk.Label(self.frame_for_time, text=" ms")
        self.label_time_.pack(side=tk.RIGHT,padx=10, pady=10)

        # frame for forkward key
        self.frame_forward_key = tk.Frame(self.img_settings)
        self.frame_forward_key.pack(padx=10, pady=5)
        self.label_forward_key = tk.Label(self.frame_forward_key, text="Forward Key: ")
        self.label_forward_key.pack(side=tk.LEFT,padx=40, pady=10)
        self.check_forward = tk.BooleanVar(value=False)
        self.check_forward_button = tk.Checkbutton(self.frame_forward_key, text="True", variable=self.check_forward, command=self.allow_entry)
        self.check_forward_button.pack(side=tk.LEFT,padx=20, pady=10)
        self.entry_forward_key = tk.Entry(self.frame_forward_key)
        self.entry_forward_key.pack(side=tk.RIGHT,padx=10, pady=10)
        self.entry_forward_key.config(state=tk.DISABLED)

        # frame for backward key
        self.frame_backward_key = tk.Frame(self.img_settings)
        self.frame_backward_key.pack(padx=10, pady=5)
        self.label_backward_key = tk.Label(self.frame_backward_key, text="Backward Key: ")
        self.label_backward_key.pack(side=tk.LEFT,padx=40, pady=10)
        self.check_backward = tk.BooleanVar(value=False)
        self.check_backward_button = tk.Checkbutton(self.frame_backward_key, text="True", variable=self.check_backward, command=self.allow_entry)
        self.check_backward_button.pack(side=tk.LEFT,padx=20, pady=10)
        self.entry_backward_key = tk.Entry(self.frame_backward_key)
        self.entry_backward_key.pack(side=tk.RIGHT,padx=10, pady=10)
        self.entry_backward_key.config(state=tk.DISABLED)

        # frame for mouse click
        self.frame_mouse_click_key = tk.Frame(self.img_settings)
        self.frame_mouse_click_key.pack(padx=10, pady=5)
        self.label_mouse_click_key = tk.Label(self.frame_mouse_click_key, text="Use mouse ? ")
        self.label_mouse_click_key.pack(side=tk.LEFT,padx=65, pady=10)
        self.check_mouse_click = tk.BooleanVar(value=False)
        self.check_mouse_click_button = tk.Checkbutton(self.frame_mouse_click_key, text="True", variable=self.check_mouse_click)
        self.check_mouse_click_button.pack(side=tk.LEFT,padx=65, pady=10)

        self.canvas = tk.Canvas(self.root,bg = "black")
        self.canvas.place(x=50, y=350,width=400)

    def close_app(self):
        self.root.destroy()

    def load_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        self.file_path = file_paths
        if file_paths:
            self.images = [Image.open(file_path) for file_path in file_paths]
            self.show_image()


    def prev_image(self):

        if self.check_entry() == False :
            return
        else:
            settings = self.check_entry()
            settings['current_image_index'] = self.current_image_index
            self.config_settings(settings)
            
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()


    def next_image(self):
        
        if self.check_entry() == False :
            return
        else:
            settings = self.check_entry()
            settings['current_image_index'] = self.current_image_index
            self.config_settings(settings)

        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_image()


    def config_settings(self,settings):
        if len(self.list_images_with_config) != 0:
            already_in = False
            for dict in self.list_images_with_config:
                if dict.get("current_image_index") == settings.get("current_image_index"):
                    already_in = True
                    dict['time'] = settings['time']
                    dict['forward'] = settings['forward']
                    dict['backward'] = settings['backward']
                    dict['mouse_click'] = settings['mouse_click']
                    break
            if not already_in:
                self.list_images_with_config.append(settings) 
        else:
            self.list_images_with_config.append(settings)


    def show_image(self):
        self.canvas.delete("all")
        image = self.images[self.current_image_index]
        aspect_ratio = image.width / image.height
        max_canvas_width = self.root.winfo_width()
        max_canvas_height = self.root.winfo_height() - self.img_settings.winfo_height()  # Exclude the height of the button frame
        if image.width > max_canvas_width or image.height > max_canvas_height:
            # If the image is larger than the canvas, resize it while maintaining aspect ratio
            if max_canvas_width / max_canvas_height < aspect_ratio:
                new_width = max_canvas_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_canvas_height
                new_width = int(new_height * aspect_ratio)
            image = image.resize((new_width, new_height))

        img = ImageTk.PhotoImage(image)
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img


    def check_entry(self):

        settings = {}
        
        if self.entry_time.cget('state') != "disabled":
            if not self.entry_time.get().isdigit():
                messagebox.showerror("Error", "The time must be number format !!!")
                return False
            else:
                settings["time"] = self.entry_time.get()
        else:
            settings["time"] = None

        if self.entry_forward_key.cget('state') != "disabled":  
            if len(self.entry_forward_key.get()) != 1:
                messagebox.showerror("Error", "Only one Forward key allowed !!!")
                return False
            else:
                settings["forward"] = self.entry_forward_key.get()
        else:
            settings["forward"] = None

        if self.entry_backward_key.cget('state') != "disabled":    
            if len(self.entry_backward_key.get()) != 1:
                messagebox.showerror("Error", "Only one Backward key allowed !!!")
                return False
            else:
                settings["backward"] = self.entry_backward_key.get()
        else:
            settings["backward"] = None

        if (self.entry_forward_key.cget('state') != "disabled") and ( self.entry_forward_key.cget('state') != "disabled") and (self.entry_backward_key.get() == self.entry_forward_key.get()):
            messagebox.showerror("Error", "Backward and Forward Key must not be the same !!!")
            return False
        
        settings["mouse_click"] = self.check_mouse_click.get()

        return settings
  

    def allow_entry(self):

        if self.check_time.get():
            self.entry_time.config(state=tk.NORMAL)  
        else:
            self.entry_time.delete(0, tk.END)  
            self.entry_time.config(state=tk.DISABLED)
        
        if self.check_forward.get():
            self.entry_forward_key.config(state=tk.NORMAL)  
        else:
            self.entry_forward_key.delete(0, tk.END)  
            self.entry_forward_key.config(state=tk.DISABLED)
        
        if self.check_backward.get():
            self.entry_backward_key.config(state=tk.NORMAL)  
        else:
            self.entry_backward_key.delete(0, tk.END)  
            self.entry_backward_key.config(state=tk.DISABLED)
    

    def start_presentation(self):
        if self.check_entry() == False :
            return
        else:
            settings = self.check_entry()
            settings['current_image_index'] = self.current_image_index
            self.config_settings(settings)
        presentation_window = tk.Toplevel(self.root,bg = "black")
        ppt_style = ImageConfiguration(presentation_window,self.entry_user.get(),self.file_path,self.list_images_with_config)
        presentation_window.mainloop()

def main():
    root = tk.Tk()
    app = Configuration(root)
    root.mainloop()

if __name__ == "__main__":
    main()