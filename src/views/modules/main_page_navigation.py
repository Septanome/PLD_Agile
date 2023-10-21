from enum import Enum

from src.controllers.navigator import Navigator, Route
from src.views.main_page.add_delivery_address_page import \
    AddDeliveryAddressPage
from src.views.main_page.add_delivery_time_window_page import \
    AddDeliveryTimeWindowPage
from src.views.main_page.confirm_delivery_address_page import \
    ConfirmDeliveryAddressPage
from src.views.main_page.current_tour_page import CurrentTourPage
from src.views.main_page.select_delivery_man_page import SelectDeliveryManPage


class MainPageNavigationRoutes(Enum):
    CURRENT_TOUR = "current_tour"
    ADD_DELIVERY_ADDRESS = "add_delivery_address"
    CONFIRM_DELIVERY_ADDRESS = "confirm_delivery_address"
    ADD_DELIVERY_TIME_WINDOW = "add_delivery_time_window"
    SELECT_DELIVERY_MAN_PAGE = "select"


main_page_navigation = Navigator[MainPageNavigationRoutes](
    routes=[
        Route(
            name=MainPageNavigationRoutes.CURRENT_TOUR,
            widget=CurrentTourPage,
        ),
        Route(
            name=MainPageNavigationRoutes.ADD_DELIVERY_ADDRESS,
            widget=AddDeliveryAddressPage,
        ),
        Route(
            name=MainPageNavigationRoutes.CONFIRM_DELIVERY_ADDRESS,
            widget=ConfirmDeliveryAddressPage,
        ),
        Route(
            name=MainPageNavigationRoutes.ADD_DELIVERY_TIME_WINDOW,
            widget=AddDeliveryTimeWindowPage,
        ),
        Route(
            name=MainPageNavigationRoutes.SELECT_DELIVERY_MAN_PAGE,
            widget=SelectDeliveryManPage,
        ),
    ],
    default_name=MainPageNavigationRoutes.CURRENT_TOUR,
)