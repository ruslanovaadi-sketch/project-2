import flet as ft


def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT

    items = []

    list_view = ft.Column()
    counter_text = ft.Text()

    def refresh_list(filter_type="all"):
        list_view.controls.clear()

        bought = 0

        for item in items:
            name, qty, done = item

            if done:
                bought += 1

            if filter_type == "done" and not done:
                continue
            if filter_type == "not_done" and done:
                continue

            def toggle_done(e, item=item):
                items[2] = e.control.value
                refresh_list(dropdown.value)

            def delete_item(e, item=item):
                items.remove(item)
                refresh_list(dropdown.value)

            list_view.controls.append(
                ft.Row(
                    controls=[
                        ft.Checkbox(value=done, on_change=toggle_done),
                        ft.Text(f"{name} (x{qty})", expand=True),
                        ft.IconButton(ft.Icons.DELETE, on_click=delete_item),
                    ]
                )
            )

        counter_text.value = f"Куплено: {bought} / {len(items)}"
        page.update()

    def add_item(e):
        if not name_input.value:
            return

        qty = int(qty_input.value) if qty_input.value else 1
        items.append([name_input.value, qty, False])

        name_input.value = ""
        qty_input.value = "1"

        refresh_list(dropdown.value)

    def filter_changed(e):
        refresh_list(e.control.value)

    name_input = ft.TextField(label="Товар", expand=True)
    qty_input = ft.TextField(label="Количество", width=120, value="1")

    add_btn = ft.ElevatedButton("ADD", icon=ft.Icons.ADD, on_click=add_item)

    dropdown = ft.Dropdown(
        value="all",
        options=[
            ft.dropdown.Option("all", "Все"),
            ft.dropdown.Option("done", "Купленные"),
            ft.dropdown.Option("not_done", "Непокупленные"),
        ],
        on_change=filter_changed,
        width=200,
    )

    page.add(
        ft.Text("Список покупок", size=25),
        ft.Row([name_input, qty_input, add_btn]),
        ft.Row([dropdown, counter_text]),
        list_view,
    )

    refresh_list()


ft.app(target=main)
