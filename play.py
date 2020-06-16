from tkinter import *
from PIL import Image,ImageTk
from random import randint

MOVES_PER_SECOND=15
GAME_SPEED=1000 // MOVES_PER_SECOND

class Snake(Canvas):
    def __init__(self, **kw):
        super().__init__(width=600,height=620,background='black',highlightthickness=0,**kw)

        self.snake_positions=[(100,100),(80,100),(60,100)]
        self.food_position=self.set_new_food_position()
        self.score=0
        self.direction='Right'

        self.bind_all('<Key>',self.on_key_press)

        self.load_assets()
        self.create_objects()
        self.after(GAME_SPEED,self.perform_actions)

    def load_assets(self):
        try:
            self.snake = Image.open('SnakeImages/snake_head.png')
            self.snakeTk = ImageTk.PhotoImage(self.snake)

            self.food = Image.open('SnakeImages/food.png')
            self.foodTk = ImageTk.PhotoImage(self.food)

        except Exception as e:
            print(e)
            root.destroy()
    def create_objects(self):

        for x_posistion,y_position in self.snake_positions:
            self.create_image(x_posistion,y_position, image=self.snakeTk,tag='snake')
        self.create_image(self.food_position[0],self.food_position[1],image=self.foodTk,
                          tag='food')
        self.create_text(45,12,text='Score: {}'.format(self.score),tag='score',fill='white',font='abc 14')
        self.create_rectangle(7,27,593,613,outline='#525d69')

    def move_snake(self):
        head_x_position, head_y_position=self.snake_positions[0]

        if(self.direction=='Left'):
            new_head_position = (head_x_position - 20, head_y_position)
        elif(self.direction=='Right'):
            new_head_position = (head_x_position + 20, head_y_position)
        elif(self.direction=='Up'):
            new_head_position = (head_x_position, head_y_position - 20)
        elif(self.direction=='Down'):
            new_head_position = (head_x_position, head_y_position + 20)

        self.snake_positions= [new_head_position] + self.snake_positions[:-1]
        for segment,position in zip(self.find_withtag('snake'),self.snake_positions):
            self.coords(segment,position)

    def perform_actions(self):
        if(self.check_collisions()):
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED,self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (
            head_x_position <=0 or head_x_position >=600
            or head_y_position <=20 or head_y_position >=620
            or (head_x_position,head_y_position) in self.snake_positions[1:]
        )
    def on_key_press(self,e):
        new_direction=e.keysym
        if(new_direction in ['Left','Right','Up','Down']):
            if(self.direction in ['Right','Left'] and new_direction in ['Right','Left']):
                return
            elif(self.direction in ['Up','Down'] and new_direction in ['Up','Down']):
                return
            self.direction=new_direction
    def check_food_collision(self):
        if(self.snake_positions[0]==self.food_position):
            self.score+=1
            if(self.score % 5 == 0):
                global MOVES_PER_SECOND
                MOVES_PER_SECOND -=5
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(*self.snake_positions[-1],image=self.snakeTk, tag='snake')
            self.itemconfig(self.find_withtag('score'), text='Score: {}'.format(self.score),tag='score')
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag('food'),self.food_position)

    def set_new_food_position(self):
        while True:
            x_position=randint(1,29) * 20
            y_position=randint(3,30) * 20

            new_food_position = (x_position,y_position)

            if new_food_position not in self.snake_positions:
                return new_food_position

    def end_game(self):
        self.delete(ALL)
        self.create_text(self.winfo_width()//2, self.winfo_height()//2,
                         text='Game Over! Your Score: {}'.format(self.score),
                         fill='white', font='abc 20 bold italic underline')


root=Tk()
root.title('Snake Game by SAGAR GUGLANI')
root.resizable(False,False)

play=Snake()
play.pack()

root.mainloop()