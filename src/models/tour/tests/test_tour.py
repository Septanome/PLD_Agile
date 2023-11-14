import unittest

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map.intersection import Intersection
from src.models.map.segment import Segment
from src.models.tour import ComputedDelivery, ComputedTour, DeliveryRequest, TourRequest
from src.models.tour.delivery_location import DeliveryLocation


class TestDeliveryLocation(unittest.TestCase):
    def test_should_create(self):
        intersection = Intersection(1.0, 1.0, 1.0)
        segment = Segment(0, "", intersection, intersection, 1.0)
        assert DeliveryLocation(segment, 0.0)

    def test_should_not_create(self):
        with self.assertRaises(TypeError):
            DeliveryLocation()


class TestDeliveryRequest(unittest.TestCase):
    def test_should_create(self):
        intersection = Intersection(1.0, 1.0, 1.0)
        segment = Segment(0, "", intersection, intersection, 1.0)
        location = DeliveryLocation(segment, 0.0)
        assert DeliveryRequest(location, 0)

    def test_should_not_create(self):
        with self.assertRaises(TypeError):
            DeliveryRequest()


class TestComputedDelivery(unittest.TestCase):
    def test_should_create(self):
        intersection = Intersection(1.0, 1.0, 1.0)
        segment = Segment(0, "", intersection, intersection, 1.0)
        delivery_location = DeliveryLocation(segment, 0.0)
        assert ComputedDelivery(delivery_location, 0.0)

    def test_should_not_create(self):
        with self.assertRaises(TypeError):
            ComputedDelivery()


class TestTourRequest(unittest.TestCase):
    def test_should_create(self):
        delivery_man = DeliveryMan("", [])
        assert TourRequest([], {}, delivery_man, "red")

    def test_should_not_create(self):
        with self.assertRaises(TypeError):
            TourRequest()


class TestComputedTour(unittest.TestCase):
    def test_should_create(self):
        delivery_man = DeliveryMan("", [])
        assert ComputedTour([], delivery_man, [], 1.0, "")

    def test_should_not_create(self):
        with self.assertRaises(TypeError):
            ComputedTour()
