from dataclasses import dataclass, field
from typing import Dict, List
from uuid import UUID

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map import Segment
from src.models.tour.delivery import (
    ComputedDelivery,
    Delivery,
    DeliveryID,
    DeliveryRequest,
)

TourID = UUID
"""Type alias for Tour ID
"""


@dataclass
class Tour:
    """Base class for tour. This represent a tour that can be request or computed."""

    id: TourID
    """ID of the tour. This ID is the same as its DeliveryMan ID.
    """

    deliveries: Dict[DeliveryID, Delivery]
    """Map of deliveries of the tour identified by their ID
    """

    delivery_man: DeliveryMan
    """Delivery man completing the tour
    """

    color: str
    """Color to use to display the tour
    """


@dataclass
class TourRequest(Tour):
    """Represents a tour request that has a list of delivery requests."""

    deliveries: Dict[DeliveryID, DeliveryRequest]
    """Map of delivery requests of the tour identified by their ID
    """


@dataclass
class ComputedTour(Tour):
    """Represents a computed tour that has a list of computed deliveries and a route."""

    deliveries: Dict[DeliveryID, ComputedDelivery]
    """Map of computed deliveries of the tour identified by their ID
    """

    route: List[Segment]
    """List of segments of the route
    """

    @staticmethod
    def create_from_request(
        tour_request: TourRequest,
        deliveries: Dict[DeliveryID, ComputedDelivery],
        route: List[Segment],
    ) -> "ComputedTour":
        """Creates an instance of ComputedTour from a TourRequest, a list of computed deliveries and a route.

        Args:
            tour_request (TourRequest): Tour request to create the computed tour from
            deliveries (Dict[DeliveryID, ComputedDelivery]): Map of computed deliveries of the tour identified by their ID
            route (List[Segment]): List of segments of the route

        Returns:
            ComputedTour: Created instance
        """

        return ComputedTour(
            id=tour_request.id,
            deliveries=deliveries,
            delivery_man=tour_request.delivery_man,
            route=route,
            color=tour_request.color,
        )