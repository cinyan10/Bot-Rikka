from PIL import Image, ImageDraw, ImageFont


def generate_server_usage_image(cpu_usage, memory_usage, disk_usage):
    # Create a blank image with a white background
    width, height = 400, 150
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Define colors for the bars
    cpu_color = (255, 0, 0)  # Red for CPU
    memory_color = (0, 255, 0)  # Green for Memory
    disk_color = (0, 0, 255)  # Blue for Disk

    # Add gradients to the percentage bars
    def draw_gradient_bar(draw, x1, y1, x2, y2, color):
        for i in range(100):
            gradient_color = (
                int(color[0] * (1 - i / 100)),
                int(color[1] * (1 - i / 100)),
                int(color[2] * (1 - i / 100))
            )
            draw.rectangle([(x1, y1 + i), (x2, y1 + i + 1)], fill=gradient_color)

    # Draw CPU usage bar
    cpu_bar_width = int(cpu_usage * (width - 40))
    draw_gradient_bar(draw, 20, 20, 20 + cpu_bar_width, 40, cpu_color)
    draw.text((30, 30), f"CPU: {cpu_usage:.2%}", fill="black", font=ImageFont.truetype("arial.ttf", 12))

    # Draw Memory usage bar
    memory_bar_width = int(memory_usage * (width - 40))
    draw_gradient_bar(draw, 20, 60, 20 + memory_bar_width, 80, memory_color)
    draw.text((30, 70), f"Memory: {memory_usage:.2%}", fill="black", font=ImageFont.truetype("arial.ttf", 12))

    # Draw Disk usage bar
    disk_bar_width = int(disk_usage * (width - 40))
    draw_gradient_bar(draw, 20, 100, 20 + disk_bar_width, 120, disk_color)
    draw.text((30, 110), f"Disk: {disk_usage:.2%}", fill="black", font=ImageFont.truetype("arial.ttf", 12))

    # Save the image to a file or return it as needed
    image.save("server_usage.png")  # Save as a file
    # image.show()  # Display the image (uncomment if needed)


# Example usage:
cpu_usage = 0.75  # 75% CPU usage
memory_usage = 0.60  # 60% Memory usage
disk_usage = 0.40  # 40% Disk usage
generate_server_usage_image(cpu_usage, memory_usage, disk_usage)
