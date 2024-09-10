import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Function to convert and resize image
def convert_image(input_folder, output_folder, conversion_type, target_size_kb=None, quality=None):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if (conversion_type == "jpg_to_png" and (filename.endswith(".jpg") or filename.endswith(".jpeg"))) or \
           (conversion_type == "png_to_jpg" and filename.endswith(".png")):

            img = Image.open(os.path.join(input_folder, filename))

            # Determine the output filename and format
            if conversion_type == "jpg_to_png":
                output_filename = os.path.splitext(filename)[0] + ".png"
                output_format = "PNG"
            elif conversion_type == "png_to_jpg":
                output_filename = os.path.splitext(filename)[0] + ".jpg"
                output_format = "JPEG"

            # Save the image with the appropriate format and quality
            output_path = os.path.join(output_folder, output_filename)

            if target_size_kb:
                compress_image(img, output_path, output_format, target_size_kb)
            else:
                img.save(output_path, output_format, quality=quality)
                print(f"Converted {filename} to {output_filename}")

def compress_image(image, output_path, output_format, target_size_kb):
    quality = 95  # Start with high quality
    min_quality = 10
    step = 5

    while quality >= min_quality:
        # Save image with the current quality
        image.save(output_path, output_format, quality=quality)
        
        # Check the size of the saved file
        file_size_kb = os.path.getsize(output_path) / 1024  # Get size in KB
        print(f"Trying quality {quality}, file size: {file_size_kb:.2f} KB")

        if file_size_kb <= target_size_kb:
            print(f"Successfully compressed image to {file_size_kb:.2f} KB")
            break
        else:
            quality -= step  # Decrease quality and try again

    if quality < min_quality:
        print(f"Could not reach the target size of {target_size_kb} KB. Final size: {file_size_kb:.2f} KB")

# Function to launch the UI
def main_ui():
    def browse_input_folder():
        folder_selected = filedialog.askdirectory()
        input_folder_var.set(folder_selected)

    def browse_output_folder():
        folder_selected = filedialog.askdirectory()
        output_folder_var.set(folder_selected)

    def start_conversion():
        input_folder = input_folder_var.get()
        output_folder = output_folder_var.get()
        conversion_type = conversion_type_var.get()
        
        if conversion_type == '1':
            conversion_type_str = "jpg_to_png"
        elif conversion_type == '2':
            conversion_type_str = "png_to_jpg"
        else:
            messagebox.showerror("Error", "Invalid conversion type selected!")
            return

        target_size_kb = None
        if size_checkbox_var.get() == 1:
            target_size_kb = simpledialog.askinteger("Target Size", "Enter the desired file size in KB:")

        # Map quality levels (1-5) to appropriate quality percentages (10-100)
        quality = None
        if quality_checkbox_var.get() == 1:
            quality_level = simpledialog.askinteger("Image Quality", "Enter quality level (1-5):")
            if 1 <= quality_level <= 5:
                quality_mapping = {
                    1: 10,  # Low quality
                    2: 30,
                    3: 50,
                    4: 75,
                    5: 95   # High quality
                }
                quality = quality_mapping[quality_level]
            else:
                messagebox.showerror("Error", "Quality level must be between 1 and 5!")
                return

        convert_image(input_folder, output_folder, conversion_type_str, target_size_kb, quality)
        messagebox.showinfo("Success", "Conversion completed!")

    # Create the main window
    window = tk.Tk()
    window.title("Image Converter")

    # Input and Output Folder Selection
    input_folder_var = tk.StringVar()
    output_folder_var = tk.StringVar()

    tk.Label(window, text="Input Folder:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(window, textvariable=input_folder_var, width=40).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(window, text="Browse", command=browse_input_folder).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(window, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(window, textvariable=output_folder_var, width=40).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(window, text="Browse", command=browse_output_folder).grid(row=1, column=2, padx=10, pady=10)

    # Conversion Type Selection
    tk.Label(window, text="Choose conversion type:").grid(row=2, column=0, padx=10, pady=10)
    conversion_type_var = tk.StringVar(value='1')
    tk.Radiobutton(window, text="JPG to PNG", variable=conversion_type_var, value='1').grid(row=2, column=1, padx=10, pady=10)
    tk.Radiobutton(window, text="PNG to JPG", variable=conversion_type_var, value='2').grid(row=2, column=2, padx=10, pady=10)

    # Checkbox for File Size and Quality options
    size_checkbox_var = tk.IntVar()
    quality_checkbox_var = tk.IntVar()

    tk.Checkbutton(window, text="Set target file size (KB)", variable=size_checkbox_var).grid(row=3, column=1, padx=10, pady=10)
    tk.Checkbutton(window, text="Set image quality (1-5)", variable=quality_checkbox_var).grid(row=4, column=1, padx=10, pady=10)

    # Start Conversion Button
    tk.Button(window, text="Start Conversion", command=start_conversion).grid(row=5, column=1, padx=10, pady=20)

    window.mainloop()

if __name__ == "__main__":
    main_ui()
