import turtle
import math

wn = turtle.Screen()
wn.setup(width=600, height=600)
wn.bgcolor("black")
wn.title("Tunnel Love - Fida")

t = turtle.Turtle()
t.hideturtle()
t.speed(0) 
t.color("#ff3366") 
t.pensize(3) 

def heart_x(k):
    return 15 * math.sin(k)**3

def heart_y(k):
    return 12 * math.cos(k) - 5*math.cos(2*k) - 2*math.cos(3*k) - math.cos(4*k)

def main():
    try:
        total_layers = 30
        
        for layer in range(total_layers):
            t.penup()
            
            scale = layer * 0.8 
            
            t.goto(heart_x(0) * scale, heart_y(0) * scale)
            t.pendown()
            
            for i in range(0, 361, 5): 
                k = math.radians(i)
                x = heart_x(k) * scale
                y = heart_y(k) * scale
                t.goto(x, y)
        
        wn.mainloop()
        
    except turtle.Terminator:
        pass 

if __name__ == "__main__":
    main()