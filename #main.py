# importar o App,
# importar Builder (GUI), interface
# criar o app
# criar a função build

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.button import Button
from datetime import datetime, timedelta

class TaskCheck(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_layouts = []  # Lista para armazenar os layouts das tarefas
        self.num_tasks = 5  # Número inicial de tarefas

    def build(self):
        root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Adicionando um layout para as tarefas
        tasks_layout = BoxLayout(orientation='vertical', spacing=10)

        # Criando e adicionando tarefas à lista
        self.create_tasks()

        # Adicionando layouts das tarefas ao layout das tarefas
        for layout in self.task_layouts:
            tasks_layout.add_widget(layout)

        # Adicionando o layout das tarefas ao root layout
        root.add_widget(tasks_layout)

        # Adicionando botões para adicionar e remover tarefas
        add_button = Button(text="Adicionar Tarefa", size_hint=(1, None), height=40)
        add_button.bind(on_press=self.add_task)

        remove_button = Button(text="Remover Última Tarefa", size_hint=(1, None), height=40)
        remove_button.bind(on_press=self.remove_task)

        root.add_widget(add_button)
        root.add_widget(remove_button)

        return root

    def create_tasks(self):
        # Criar layouts de tarefas e adicionar à lista
        self.task_layouts = []
        for i in range(self.num_tasks):
            task_layout = BoxLayout(orientation='horizontal', spacing=10)

            # Caixa de seleção para fazer check
            check_box = CheckBox(size_hint_x=None, width=40)

            # Caixa de texto para a tarefa
            task_input = TextInput(hint_text=f'Tarefa {i+1}', multiline=False, size_hint_x=0.6)

            # Spinner para selecionar o período do check
            period_spinner = Spinner(
                text='Diária',
                values=('Diária', 'Semanal', 'Mensal'),
                size_hint_x=0.3
            )

            # Adicionando widgets à linha da tarefa
            task_layout.add_widget(check_box)
            task_layout.add_widget(task_input)
            task_layout.add_widget(period_spinner)

            self.task_layouts.append(task_layout)

    def on_start(self):
        # Verificar os checks ao iniciar o aplicativo
        self.check_tasks()

    def check_tasks(self):
        # Verificar os checks periodicamente
        Clock.schedule_interval(self.update_checks, 60)  # Verifica a cada minuto

    def update_checks(self, dt):
        # Atualizar os checks com base no período configurado
        for layout in self.task_layouts:
            check_box = layout.children[0]
            period_spinner = layout.children[2]
            period = period_spinner.text.lower()

            # Verificar se a tarefa foi marcada e atualizar o status com base no período
            if check_box.active:
                if period == "diária":
                    # Verificar se o check foi feito hoje
                    check_date = datetime.strptime(check_box.group, "%Y-%m-%d %H:%M:%S.%f")
                    today = datetime.now().date()
                    if check_date.date() != today:
                        check_box.active = False
                elif period == "semanal":
                    # Verificar se o check foi feito esta semana
                    check_date = datetime.strptime(check_box.group, "%Y-%m-%d %H:%M:%S.%f")
                    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).date()
                    if check_date.date() < week_start:
                        check_box.active = False
                elif period == "mensal":
                    # Verificar se o check foi feito neste mês
                    check_date = datetime.strptime(check_box.group, "%Y-%m-%d %H:%M:%S.%f")
                    if check_date.month != datetime.now().month:
                        check_box.active = False

    def add_task(self, instance):
        # Adicionar uma nova tarefa
        if self.num_tasks < 10:  # Limitar a 10 tarefas
            task_layout = BoxLayout(orientation='horizontal', spacing=10)

            check_box = CheckBox(size_hint_x=None, width=40)
            task_input = TextInput(hint_text=f'Tarefa {self.num_tasks+1}', multiline=False, size_hint_x=0.6)
            period_spinner = Spinner(
                text='Diária',
                values=('Diária', 'Semanal', 'Mensal'),
                size_hint_x=0.3
            )

            task_layout.add_widget(check_box)
            task_layout.add_widget(task_input)
            task_layout.add_widget(period_spinner)

            # Adicionando a nova tarefa acima dos botões de adicionar/remover
            self.root.children[-1].add_widget(task_layout, len(self.root.children[-1].children)-2)
            self.task_layouts.append(task_layout)
            self.num_tasks += 1

    def remove_task(self, instance):
        # Remover a última tarefa
        if self.num_tasks > 1:  # Mantém pelo menos uma tarefa
            task_layout = self.task_layouts.pop()
            self.root.children[-1].remove_widget(task_layout)  # Removendo a última tarefa do último widget do root layout
            self.num_tasks -= 1

if __name__ == '__main__':
    TaskCheck().run()











