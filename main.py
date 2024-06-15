import flet as ft



def main(page: ft.Page):
    
    page.title = "Shablonizattor"
    page.theme_mode = ft.ThemeMode.DARK     # Как перенести параметры в init.py
    
    page.window_width = 350         # 350 min
    page.window_height = 550

    page.window_left = 200
    page.window_top = 50                   # Как перенести параметры в init.py
    
    main_icon_color="blue400"
    
    def hoverme(e):
        if e.data == "true":
            e.control.scale = ft.Scale(scale=1.1)
        else:
            e.control.scale = ft.Scale(scale=1)
        page.update()

    def move_widget(e):

            if sw_MoveVidget.value == True:
                page.window_title_bar_hidden = True
                print(sw_MoveVidget.value)
                sw_MoveVidget.value =True
            else:
                sw_MoveVidget.value = False
                page.window_title_bar_hidden = False
                print(sw_MoveVidget.value)

            page.update()
    
    def window_always_on_top(e):

            if sw_WindowTop.value == True:
                sw_WindowTop.value =True
            else:
                sw_WindowTop.value = False

            if page.window_always_on_top == False:
                page.window_always_on_top = True
            else:
                page.window_always_on_top = False
                
            page.update()
    
    def fun_addSetter(string):
        
        result_set = ""
        for i in list_clean:
            result_set += f'\ndef set_{i}(self, value):\n'
            result_set += f'\tself.{i} = value\n'

        return string + result_set
    
    def fun_addGetter(string):
        
        result_get = ""
        for i in list_clean:
            result_get += f'\ndef get_{i}(self):\n'
            result_get += f'\treturn self.{i}\n'
        
        return string + result_get
    
    def fun_make_constructor(str_line):
        
        global list_clean 
        list_clean = []
        list_ignore_elements = ['->', 'self', '__init__', 'def', 'None:']
        dicionary  = ",.()"
        str_line_clean = ""

        for i in str_line:
            if i in dicionary:
                i = i.replace(i, " ")
            str_line_clean += i

        list_elements = str_line_clean.split()
        for i in range(len(list_elements)):
            if not list_elements[i] in list_ignore_elements:
                
                list_clean.append(list_elements[i])

        str_line = "" 
        for i in list_clean:
            str_line += i + ", "

        str_result = f"def __init__(self, {str_line}) -> None: \n"
        

        list_clean_L2 = []
        for element in list_clean:
            for i in element:
                if i == "=" and i != element[-1]:
                    copy_element = element.split("=")
                    list_clean_L2.append(copy_element[0])
                    break
            else:
                    list_clean_L2.append(element)

        list_clean = list_clean_L2 # Оставить т.к. "list_clean" используется в других методах
        
        for i in list_clean:
            str_result += f"\tself.{i} = {i}\n"
            
        
        return str_result
        
    def textbox_changed(e):
        
        result = fun_make_constructor(e.control.value)
            
        if addSet.value == True:
            # print("True")
            result = fun_addSetter(result)
            
        if addGet.value == True:
            result = fun_addGetter(result)
            pass
        
        
        text_result_info.value = result
        page.update()
    
    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        light_change.label = (
            "   Light theme" if page.theme_mode == ft.ThemeMode.LIGHT else "   Dark theme"
        )
        page.update()
    
    def copy_value(e):
        # get_txt = "fdfdfdffdf"
        page.set_clipboard(text_result_info.value)
        
        pass
    
    text_result_info = ft.Text(selectable=True)
    addGet = ft.CupertinoCheckbox(label="GETTER", value=True, active_color="blue600", tooltip="Добавить Getter",)
    addSet = ft.CupertinoCheckbox(label="SETTER", value=True, active_color="blue600", tooltip="Добавить Setter",)
    light_change = ft.Switch(label="   Light theme", on_change=theme_changed)
    sw_WindowTop = ft.Switch(label="   Window always on top", on_change=window_always_on_top)
    sw_MoveVidget = ft.Switch(label="   Block moving vidget", on_change=move_widget)
    
    if page.window_width > 576:
        block_buttons = ft.Row(controls=[
            ft.Column([
                ft.Container(
                    ),
                ft.Container(expand=True,
                    content=ft.Column([
                        
                        ft.TextButton("Консструктор",icon=ft.icons.CONSTRUCTION,icon_color="blue600",on_hover=hoverme),
                        ft.TextButton("Проект",icon=ft.icons.PRODUCTION_QUANTITY_LIMITS,icon_color="blue600",),
                    ]) , 
                    
                ),
                ft.TextButton("Добавить модуль",icon=ft.icons.ADD,icon_color="green600",),
                ft.TextButton("Меню",icon=ft.icons.ARROW_BACK,icon_color="green600"),
            ]),
            ft.VerticalDivider(width=1),
        ])
    else:
        block_buttons = ft.Row([])
    
    
    tab = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        scrollable = True,
        tabs=[
           
            ft.Tab(
                tab_content=ft.Icon(ft.icons.MENU),
                content=ft.Column([
                            ft.ResponsiveRow([
                                ft.Container(
                                    ft.Column([
                                        ft.Row( alignment = ft.MainAxisAlignment.CENTER, controls=[
                                            ft.Text(value = "View settings", weight=ft.FontWeight.BOLD,),
                                            ]),
                                        
                                                light_change,
                                                sw_WindowTop,
                                                sw_MoveVidget,
                                                ]),
                                            margin=10,
                                            col={"sm": 6, "md": 4, "xl": 4},
                                            ),
                                        ],
                                        run_spacing={"xs": 10},
                            ),
                        ],scroll=ft.ScrollMode.AUTO, alignment=ft.CrossAxisAlignment.CENTER, expand=True,)
            ),
            
            ft.Tab(
                text="Python",
                content=ft.Row(controls=[
                    block_buttons,
                    ft.Column([ 
                               
                        ft.Row([
                            ft.TextField(
                            border="underline",
                            label="Укажите переменные: ",
                            on_change=textbox_changed,
                            expand=True,
                            
                            ),
                                
                            ft.IconButton(
                                        icon=ft.icons.COPY,
                                        icon_color=main_icon_color,
                                        icon_size=25,
                                        tooltip="Копировать код",
                                        on_click=copy_value
                                    ),
                                ]),     
                        
                        ft.ResponsiveRow([
                                        
                                        ft.Container(
                                            addSet,
                                            # padding=5,
                                            col={"xs": 6, "sm": 6, "xl": 6},
                                        ),
                                        ft.Container(
                                            addGet,
                                            # padding=5,
                                            col={"xs": 6, "sm": 6, "xl": 6},
                                        ),
                        ]),
                        
                        ft.Column([
                            ft.Row([
                             text_result_info,
                             
                        ],alignment=ft.MainAxisAlignment.START),
                            
                            
                            ],scroll=ft.ScrollMode.AUTO, alignment=ft.CrossAxisAlignment.CENTER, expand=True,), 
                        
                    ], alignment=ft.MainAxisAlignment.START, expand=True),],
                )
            ),
        ],
        expand=1,
    )

    page.add(tab
        )
ft.app(target=main)


