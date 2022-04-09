from tkinter import dialog
from turtle import right
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.recycleview import layout
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import mainthread
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from PIL import Image
import pandas as pd
import numpy as np
import csv
from itertools import compress
from main_solver import *
from fractions import Fraction
import pylab
from pprint import pprint
from beam_diagram_generator import *
def deflection_at_point_image(formula):
    fig = pylab.figure()
    formula=r'$'+formula+r'$'
    text = fig.text(0, 0, formula)

    # Saving the figure will render the text.
    dpi = 300
    fig.savefig('AppData\Images\deflection_at_point.png', dpi=dpi)

    # Now we can work with text's bounding box.
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    # Adjust the figure size so it can hold the entire text.
    fig.set_size_inches((width, height))

    # Adjust text's vertical position.
    dy = (bbox.ymin/float(dpi))/height
    text.set_position((0, -dy))

    # Save the adjusted text.
    fig.savefig('AppData\Images\deflection_at_point.png', dpi=dpi)
def governing_equation_image(formula):
    fig = pylab.figure()
    formula=r'$'+formula+r'$'
    text = fig.text(0, 0, formula)

    # Saving the figure will render the text.
    dpi = 300
    fig.savefig('AppData\Images\governing_equation.png', dpi=dpi)

    # Now we can work with text's bounding box.
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    # Adjust the figure size so it can hold the entire text.
    fig.set_size_inches((width, height))

    # Adjust text's vertical position.
    dy = (bbox.ymin/float(dpi))/height
    text.set_position((0, -dy))

    # Save the adjusted text.
    fig.savefig('AppData\Images\governing_equation.png', dpi=dpi)

def final_solution_image(formula):
    fig = pylab.figure()
    formula='$'+formula+'$'
    #print(formula)
    text = fig.text(0, 0, formula)
    # Saving the figure will render the text.
    dpi = 300
    fig.savefig(r'AppData\Images\final_solution.png', dpi=dpi)

    # Now we can work with text's bounding box.
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    # Adjust the figure size so it can hold the entire text.
    fig.set_size_inches((width, height))

    # Adjust text's vertical position.
    dy = (bbox.ymin/float(dpi))/height
    text.set_position((0, -dy))

    # Save the adjusted text.
    fig.savefig(r'AppData\Images\final_solution.png', dpi=dpi)

global governing_equation, final_solution, deflection_at_point

def create_load_summary():
    point_df=pd.read_csv('AppData\Files\point_load.csv')
    moment_df=pd.read_csv('AppData\Files\moment_load.csv')
    distributed_df=pd.read_csv('AppData\Files\distributed_load.csv')

    moment_df["DESCRIPTION"]='('+moment_df["MULTIPLIER"].astype(str)+')*'+'M'
    moment_df["LOCATION"]='x=('+moment_df["LOCATION"].astype(str)+')*'+'L'
    moment_df["TYPE"]="Moment Load "+(moment_df.index+1).astype(str)

    point_df["DESCRIPTION"]='('+point_df["MULTIPLIER"].astype(str)+')*'+'P'
    point_df["LOCATION"]='x=('+point_df["LOCATION"].astype(str)+')*'+'L'
    point_df["TYPE"]="Point Load "+(point_df.index+1).astype(str)

    distributed_df["TYPE"]="Distributed Load "+(distributed_df.index+1).astype(str)
    distributed_df["DESCRIPTION"]="Order="+distributed_df["ORDER"].astype(str)+" | "+"Coefficients=["+distributed_df["COEFFICIENTS"].astype(str)+"]"
    distributed_df["LOCATION"]='('+distributed_df["LEFT_LIMIT"].astype(str)+')*'+'L <= x <= '+'('+distributed_df["RIGHT_LIMIT"].astype(str)+')*'+'L'
    summary_df=pd.DataFrame(distributed_df[["TYPE","DESCRIPTION","LOCATION"]])
    summary_df=pd.concat([summary_df,point_df[["TYPE","DESCRIPTION","LOCATION"]]], ignore_index=True)
    summary_df=pd.concat([summary_df,moment_df[["TYPE","DESCRIPTION","LOCATION"]]], ignore_index=True)
    #summary_df.index += 1
    summary_df.to_csv("AppData\Files\load_summary.csv", index=False,header=False)

class SelectLoadType(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class PointLoadInput(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class MomentLoadInput(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class DistributedLoadInput(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class WindowManager(ScreenManager):
    pass
class HomeWindow(Screen):
    dialog=None
    
    def update_boundary_condition(self):
        left_boundary="fixed"
        right_boundary="free"
        if self.ids.left_fixed.active:
            left_boundary="fixed"
        elif self.ids.left_free.active:
            left_boundary="free"
        elif self.ids.left_hinged.active:
            left_boundary="hinged"
        elif self.ids.left_roller.active:
            left_boundary="roller"
        if self.ids.right_free.active:
            right_boundary="free"
        elif self.ids.right_fixed.active:
            right_boundary="fixed"
        elif self.ids.right_hinged.active:
            right_boundary="hinged"
        elif self.ids.right_roller.active:
            right_boundary="roller"
        #print(left_boundary,right_boundary)
        if left_boundary=="free" and right_boundary=="free":
            toast("Oopsie! The beam can't have both the ends as free!!")
            self.ids.right_fixed.active=True
            self.ids.left_fixed.active
            left_boundary='fixed'
            right_boundary='fixed'
        elif left_boundary=="roller" and right_boundary=="roller":
            toast("Oopsie! The beam can't have both the ends as rollers!!")
            self.ids.right_fixed.active=True
            self.ids.left_fixed.active=True
            left_boundary='fixed'
            right_boundary='fixed'
        elif left_boundary=="roller" and right_boundary=="free":
            toast("Oopsie! The beam doesn't seem to be stable!!")
            self.ids.right_fixed.active=True
            self.ids.left_fixed.active=True
            left_boundary='fixed'
            right_boundary='fixed'
        elif left_boundary=="free" and right_boundary=="roller":
            toast("Oopsie! The beam doesn't seem to be stable!!")
            self.ids.right_fixed.active=True
            self.ids.left_fixed.active=True
            left_boundary='fixed'
            right_boundary='fixed'
        elif left_boundary=="hinged" and right_boundary=="free":
            toast("Oopsie! The beam doesn't seem to be stable!!")
            self.ids.right_fixed.active=True
            self.ids.left_fixed.active=True
            left_boundary='fixed'
            right_boundary='fixed'
        elif left_boundary=="free" and right_boundary=="hinged":
            toast("Oopsie! The beam doesn't seem to be stable!!")
            self.ids.right_fixed.active=True
            self.ids.left_fixed.active=True
            left_boundary='fixed'
            right_boundary='fixed'
        boundary_df=pd.read_csv(r'AppData\Files\boundary_condition.csv', dtype=str)
        boundary_df["LEFT"].iloc[0]=left_boundary
        boundary_df["RIGHT"].iloc[0]=right_boundary
        boundary_df.to_csv(r"AppData\Files\boundary_condition.csv", index=False)
        

    def dialog_close(self,*args):
        self.dialog.dismiss(force=True)
    def refresh(self):
        self.create_datatable()
        self.update_boundary_condition()
        print("drawing started")
        draw()
        print("drawing completed")
        self.ids.beam_diagram.reload()
        #self.create_diagram()
        
    def delete_selected_loads(self):
        df=pd.read_csv("AppData\Files\load_summary.csv",header=None)
        point_df=pd.read_csv("AppData\Files\point_load.csv")
        point_df_bools=[True]*len(point_df.index)
        moment_df=pd.read_csv("AppData\Files\moment_load.csv")
        moment_df_bools=[True]*len(moment_df.index)
        distributed_df=pd.read_csv("AppData\Files\distributed_load.csv")
        distributed_df_bools=[True]*len(distributed_df.index)
        deleted_df=df[np.invert(self.active_indices)]
        for index,row in deleted_df.iterrows():
            deleting_index=""
            if "Point" in row[0]:
                for m in row[0]:
                    if m.isdigit():
                        deleting_index=deleting_index+m
                point_df_bools[int(deleting_index)-1]=False
            elif "Moment" in row[0]:
                for m in row[0]:
                    if m.isdigit():
                        deleting_index=deleting_index+m
                moment_df_bools[int(deleting_index)-1]=False
            elif "Distributed" in row[0]:
                for m in row[0]:
                    if m.isdigit():
                        deleting_index=deleting_index+m
                distributed_df_bools[int(deleting_index)-1]=False
        df=df[self.active_indices]
        if len(point_df_bools)>0: point_df=point_df[point_df_bools]
        if len(moment_df_bools)>0: moment_df=moment_df[moment_df_bools]
        if len(distributed_df_bools)>0: distributed_df=distributed_df[distributed_df_bools]
        point_df.to_csv("AppData\Files\point_load.csv",index=False)
        moment_df.to_csv("AppData\Files\moment_load.csv",index=False)
        distributed_df.to_csv("AppData\Files\distributed_load.csv",index=False)
        df.to_csv("AppData\Files\load_summary.csv",index=False,header=False)
        self.create_datatable()
    def add_new_load(self):
        if self.dialog:
            del self.dialog
        self.dialog = MDDialog(
            type="custom",
            content_cls=SelectLoadType(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="NEXT",
                    on_release=self.load_input_dialog
                ),
            ],
        )
        self.dialog.open()
    def solve(self):
        global governing_equation, final_solution, deflection_at_point
        try:
            initialise_global_variables()
            formulate_point_loads()
            formulate_moment_loads()
            formulate_distributed_loads()
            governing_equation=formulate_gde()
            final_solution=apply_boundary_conditions(solve_gde(governing_equation))
        except:
            toast("Oops! Sympy failed to solve it!!")
        
        try:
            governing_equation_image(sp.latex(governing_equation))
            #print("governing equation created")
        except:
            toast("Oh! We failed to render the governing equation")

        try:
            final_solution_image(sp.latex(final_solution))
            #print("solution image created")
        except:
            toast("Oh! We failed to render the goodlooking solution")
            formula="Sorry! We couldn't render the solution!!\nBut we guarantee it's ready, enter 'x'"
            fig = pylab.figure()
            text = fig.text(0, 0, formula)
            dpi = 300
            fig.savefig(r'AppData\Images\final_solution.png', dpi=dpi)
            bbox = text.get_window_extent()
            width, height = bbox.size / float(dpi) + 0.005
            fig.set_size_inches((width, height))
            dy = (bbox.ymin/float(dpi))/height
            text.set_position((0, -dy))
            fig.savefig(r'AppData\Images\final_solution.png', dpi=dpi)
            print(sp.latex(final_solution))
        self.parent.current="result"
    def load_input_dialog(self,*args):
        if self.dialog.content_cls.ids.point_type_selected.active:
            if self.dialog:
                self.dialog.dismiss(force=True)
                del self.dialog
            self.dialog = MDDialog(
            type="custom",
            content_cls=PointLoadInput(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=self.save_point_load_input
                ),
                ],
            )
            self.dialog.open()
        elif self.dialog.content_cls.ids.moment_type_selected.active:
            if self.dialog:
                self.dialog.dismiss(force=True)
                del self.dialog
            self.dialog = MDDialog(
            type="custom",
            content_cls=MomentLoadInput(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=self.save_moment_load_input
                ),
                ],
            )
            self.dialog.open()
        elif self.dialog.content_cls.ids.distributed_type_selected.active:
            if self.dialog:
                self.dialog.dismiss(force=True)
                del self.dialog
            self.dialog = MDDialog(
            type="custom",
            content_cls=DistributedLoadInput(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=self.save_distributed_load_input
                ),
                ],
            )
            self.dialog.open()
    def save_point_load_input(self,*args):
        point_load_magnitude=self.dialog.content_cls.ids.point_load_multiplier.text
        point_load_location=self.dialog.content_cls.ids.point_load_location.text
        with open('AppData\Files\point_load.csv','a',newline='') as file:
            csv_writer=csv.writer(file)
            csv_writer.writerow([point_load_magnitude,point_load_location])
        self.dialog_close()
        self.refresh()
        toast("The new point load has been successfully added")
    def save_moment_load_input(self,*args):
        moment_load_magnitude=self.dialog.content_cls.ids.moment_load_multiplier.text
        moment_load_location=self.dialog.content_cls.ids.moment_load_location.text
        with open('AppData\Files\moment_load.csv','a',newline='') as file:
            csv_writer=csv.writer(file)
            csv_writer.writerow([moment_load_magnitude,moment_load_location])
        self.dialog_close()
        self.refresh()
        toast("The new moment load has been successfully added")
    def save_distributed_load_input(self,*args):
        distributed_load_order=self.dialog.content_cls.ids.distributed_load_order.text
        distributed_load_coefficients=self.dialog.content_cls.ids.distributed_load_coefficients.text
        distributed_load_left_limit=self.dialog.content_cls.ids.distributed_load_left_limit.text
        distributed_load_right_limit=self.dialog.content_cls.ids.distributed_load_right_limit.text
        with open('AppData\Files\distributed_load.csv','a',newline='') as file:
            csv_writer=csv.writer(file)
            csv_writer.writerow([distributed_load_order, distributed_load_coefficients, distributed_load_left_limit, distributed_load_right_limit])
        self.dialog_close()
        self.refresh()
        toast("The new distributed load has been successfully added")
    def create_load_summary():
        point_df=pd.read_csv('AppData\Files\point_load.csv')
        moment_df=pd.read_csv('AppData\Files\moment_moment.csv')
        distributed_df=pd.read_csv('AppData\Files\distributed_load.csv')
    def create_datatable(self):
        create_load_summary()
        if self.ids.display_load_table.children:
            self.ids.display_load_table.clear_widgets()
        with open('AppData\Files\load_summary.csv', newline='') as f:
            reader = csv.reader(f)
            self.data = list(reader)
        if len(self.data)>0:
            self.active_indices=[True]*len(self.data)
            self.data_tables = MDDataTable(
                size_hint=(1, 1),
                pos_hint={"center_x": 0.5},
                #id="log_table",
                use_pagination=False,
                check=True,
                column_data=[
                    ("TYPE", dp(40)),
                    ("DESCRIPTION", dp(45)),
                    ("LOCATION", dp(40)),
                ],
                row_data=self.data,
                rows_num=int(len(self.data)),
                elevation=2,
            )
        else:
            #print("I am called")
            self.data_tables = MDDataTable(
                #size_hint=(1, 1),
                #pos_hint={"center_x": 0.5},
                #id="log_table",
                use_pagination=False,
                check=True,
                column_data=[
                    ("TYPE", dp(40)),
                    ("DESCRIPTION", dp(45)),
                    ("LOCATION", dp(40)),
                ],
                elevation=2,
            )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        self.ids.display_load_table.add_widget(self.data_tables)
        #return data_tables
    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        pass#self.clicked_index=int(instance_row.index/3)
    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        self.clicked_index=self.data.index(current_row)
        self.active_indices[self.clicked_index]=not self.active_indices[self.clicked_index]

class ResultWindow(Screen):
    dialog=None
    def on_enter(self, *args):
        self.ids.governing_equation.reload()
        self.ids.solution_image.reload()
        return super().on_enter(*args)
    def dialog_close(self,*args):
        self.dialog.dismiss(force=True)
    def back_home(self):
        self.parent.current="home"
    def evaluate_deflection(self):
        try:
            deflection_at_point=(final_solution).subs([(x,Fraction(self.ids.deflection_at_x.text)*L)])
            deflection_at_point_image(sp.latex(deflection_at_point))
            if self.dialog:
                del self.dialog
            self.dialog = MDDialog(
                type="custom",
                content_cls=DisplayDeflection(),
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        on_release=self.dialog_close
                    ),
                ],
                )
            self.dialog.open()
        except:
            toast("Oops! Something went wrong!!")
        
        
        
        
class DisplayDeflection(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.deflection_at_point.reload()


class DeflectionCalculatorApp(MDApp):
    def __init__(self, **kwargs):
        self.title="Beam Deflection Calculator"
        super().__init__(**kwargs)
    def build(self):
        main_screen=Screen()
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="BlueGray"
        main_screen.add_widget(Builder.load_file('main.kv'))
        return main_screen

DeflectionCalculatorApp().run()