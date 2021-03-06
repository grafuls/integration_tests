from navmazing import NavigateToAttribute, NavigateToSibling
from widgetastic.widget import Text
from widgetastic_manageiq import SSUIPrimarycard, SSUIAggregatecard, SSUIlist

from cfme.base.ssui import SSUIBaseLoggedInPage
from cfme.utils.appliance.implementations.ssui import (
    navigator,
    SSUINavigateStep,
    navigate_to,
    ViaSSUI
)

from . import Dashboard


class DashboardView(SSUIBaseLoggedInPage):
    title = Text(locator='//li[@class="active"]')
    dashboard_card = SSUIPrimarycard()
    aggregate_card = SSUIAggregatecard()

    def in_dashboard(self):
        return (
            self.logged_in_as_current_user and
            self.navigation.currently_selected == ["", "Dashboard"] and
            self.dashboard_card.is_displayed)

    @property
    def is_displayed(self):
        return self.in_dashboard


class MyServiceForm(SSUIBaseLoggedInPage):

    service = SSUIlist(list_name='serviceList')


class MyServicesView(MyServiceForm):
    title = Text(locator='//li[@class="active"]')

    def in_myservices(self):
        return (
            self.logged_in_as_current_user and
            self.navigation.currently_selected == ["", "My Services"])

    @property
    def is_displayed(self):
        return self.in_myservices and self.title.text == "My Services"


@Dashboard.total_service.external_implementation_for(ViaSSUI)
def total_service(self):
    """Returns the count of total services(Integer) displayed on dashboard"""

    view = navigate_to(self, 'DashboardAll')
    total_services = view.dashboard_card.get_count('Total Services')
    view = navigate_to(self, 'TotalServices')
    view.flash.assert_no_error()
    view = self.create_view(MyServicesView)
    assert view.is_displayed
    return total_services


@Dashboard.total_request.external_implementation_for(ViaSSUI)
def total_request(self):
    """Total Request cannot be clicked so this method just
    returns the total number of requests displayed on dashboard.
    """

    view = navigate_to(self, 'DashboardAll')
    total_requests = view.dashboard_card.get_count('Total Requests')
    return total_requests


@Dashboard.retiring_soon.external_implementation_for(ViaSSUI)
def retiring_soon(self):
    """Returns the count of retiring soon services displayed on dashboard"""

    view = navigate_to(self, 'DashboardAll')
    retiring_services = view.aggregate_card.get_count('Retiring Soon')
    view = navigate_to(self, 'RetiringSoon')
    view.flash.assert_no_error()
    view = self.create_view(MyServicesView)
    assert view.is_displayed
    return retiring_services


@Dashboard.current_services.external_implementation_for(ViaSSUI)
def current_service(self):
    """Returns the count of active services displayed on dashboard"""

    view = navigate_to(self, 'DashboardAll')
    current_services = view.aggregate_card.get_count('Current Services')
    view = navigate_to(self, 'CurrentServices')
    view.flash.assert_no_error()
    view = self.create_view(MyServicesView)
    assert view.is_displayed
    return current_services


@Dashboard.retired_services.external_implementation_for(ViaSSUI)
def retired_service(self):
    """Returns the count of retired services displayed on dashboard"""

    view = navigate_to(self, 'DashboardAll')
    retired_services = view.aggregate_card.get_count('Retired Services')
    view = navigate_to(self, 'RetiredServices')
    view.flash.assert_no_error()
    view = self.create_view(MyServicesView)
    assert view.is_displayed
    return retired_services


@Dashboard.monthly_charges.external_implementation_for(ViaSSUI)
def monthly_charges(self):
    """Returns the chargeback data displayed on dashboard"""

    view = navigate_to(self, 'DashboardAll')
    return view.aggregate_card.get_count('Monthly Charges - This Month To Date')


@navigator.register(Dashboard, 'DashboardAll')
class DashboardAll(SSUINavigateStep):
    VIEW = DashboardView

    prerequisite = NavigateToAttribute('appliance.server', 'LoggedIn')

    def step(self, *args, **kwargs):
        self.prerequisite_view.navigation.select('Dashboard')


@navigator.register(Dashboard, 'TotalServices')
class TotalServices(SSUINavigateStep):
    VIEW = MyServicesView

    prerequisite = NavigateToSibling('DashboardAll')

    def step(self, *args, **kwargs):
        self.prerequisite_view.dashboard_card.click_at("Total Services")


@navigator.register(Dashboard, 'RetiringSoon')
class RetiringSoon(SSUINavigateStep):
    VIEW = MyServicesView

    prerequisite = NavigateToSibling('DashboardAll')

    def step(self, *args, **kwargs):
        self.prerequisite_view.aggregate_card.click_at("Retiring Soon")


@navigator.register(Dashboard, 'CurrentServices')
class CurrentServices(SSUINavigateStep):
    VIEW = MyServicesView

    prerequisite = NavigateToSibling('DashboardAll')

    def step(self, *args, **kwargs):
        self.prerequisite_view.aggregate_card.click_at("Current Services")


@navigator.register(Dashboard, 'RetiredServices')
class RetiredServices(SSUINavigateStep):
    VIEW = MyServicesView

    prerequisite = NavigateToSibling('DashboardAll')

    def step(self, *args, **kwargs):
        self.prerequisite_view.aggregate_card.click_at("Retired Services")
