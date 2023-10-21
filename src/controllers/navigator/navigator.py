from enum import Enum
from typing import Generic, List, Optional, Tuple, TypeVar

from PyQt6.QtWidgets import QLabel, QStackedWidget, QVBoxLayout, QWidget
from reactivex import Observable
from reactivex.operators import map
from reactivex.subject import BehaviorSubject

from src.controllers.navigator.navigator_config import NavigatorConfig
from src.controllers.navigator.page import Page
from src.controllers.navigator.route import Route

RouteName = TypeVar("RouteName", Enum, str)


class Navigator(Generic[RouteName]):
    __history_stack: BehaviorSubject[List[RouteName]]
    __routes: List[Route]
    __not_found_widget: Optional[QWidget]
    __config: NavigatorConfig

    def __init__(
        self,
        routes: List[Route],
        default_name: RouteName,
        not_found_widget: Optional[QWidget] = None,
        config: NavigatorConfig = NavigatorConfig(),
    ) -> None:
        """Navigator

        Parameters:
            routes (List[Route]): List of routes
            default_name (str, optional): Default route name. Defaults to "".
            not_found_widget (Optional[QWidget], optional): Widget to show when route is not found. Defaults to None.

        Returns:
            None
        """

        self.__routes = routes
        self.__history_stack = BehaviorSubject([default_name])
        self.__not_found_widget = not_found_widget
        self.__config = config

    @property
    def history_stack(self) -> Observable[List[str]]:
        """Returns the history stack as an observable

        Returns:
            Observable[List[str]]: Observable of the history stack
        """
        return self.__history_stack

    @property
    def current_route_name(self) -> Observable[str]:
        """Returns the current route name as an observable

        Returns:
            Observable[str]: Observable of the current route name
        """
        return self.__history_stack.pipe(map(lambda _: self.__history_stack.value[-1]))

    @property
    def current_route(self) -> Observable[Tuple[int, Route]]:
        """Returns the current route resolved from the current route name as an observable

        Returns:
            Observable[Tuple[int, Route]]: Observable with a tuple of the index of the route and the route
        """
        return self.current_route_name.pipe(map(self.__resolve_route))

    @property
    def can_go_back(self) -> Observable[bool]:
        """Returns an observable that indicates if the navigator can go back

        Returns:
            Observable[bool]: Observable that indicates if the navigator can go back
        """
        return self.__history_stack.pipe(
            map(lambda _: len(self.__history_stack.value) > 1)
        )

    def push(self, name: RouteName) -> None:
        """Add a route to the history stack

        Args:
            name (RouteName): Name of the route to add
        """
        if (
            not self.__config.allow_push_same_route
            and self.__history_stack.value[-1] == name
        ):
            return

        self.__history_stack.on_next(self.__history_stack.value + [name])

    def pop(self) -> None:
        """Remove last route from the history stack"""
        if len(self.__history_stack.value) == 1:
            raise IndexError("Can't pop last route")

        self.__history_stack.on_next(self.__history_stack.value[:-1])

    def replace(self, name: RouteName) -> None:
        """Replace last route from the stack

        Args:
            name (RouteName): Name of the route to replace
        """
        if (
            not self.__config.allow_replace_same_route
            and self.__history_stack.value[-1] == name
        ):
            return

        self.__history_stack.on_next(self.__history_stack.value[:-1] + [name])

    def get_router_outlet(self) -> QWidget:
        """Build a router outlet that shows the current route's widget

        Returns:
            QWidget: Widget that shows the current route's widget
        """
        widget = QStackedWidget()

        for route in self.__routes:
            widget.addWidget(route.widget())

        widget.addWidget(self.__not_found_widget or self.__build_not_found_widget())

        def on_route_change(res: Tuple[int, Route]) -> None:
            index, _ = res
            previous_widget = widget.currentWidget()
            next_widget = widget.widget(index)

            if isinstance(previous_widget, Page) and previous_widget != next_widget:
                previous_widget.on_page_leave()

            if isinstance(next_widget, Page):
                next_widget.on_page_enter()

            widget.setCurrentIndex(index)

        self.current_route.subscribe(on_route_change)

        return widget

    def __match_name(self, route_name: str, search_name: str) -> bool:
        return route_name == search_name

    def __resolve_route(self, name: str) -> Tuple[int, Route]:
        for i, route in enumerate(self.__routes):
            if self.__match_name(route.name, name):
                return (i, route)

        return (len(self.__routes), Route(name=name, widget=self.__not_found_widget))

    def __build_not_found_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Error: Route not found")

        layout.addWidget(label)
        widget.setLayout(layout)

        return widget