/** @odoo-module */
import { registry } from "@web/core/registry"
import { KmPetronadKpiCard } from "./kpi_card"
const { Component } = owl

export class KmPetronadDashboard extends Component {
    setup(){
    }
}

KmPetronadDashboard.template = "km_petronad.dashboard_view"
KmPetronadDashboard.components = { KmPetronadKpiCard }
registry.category("actions").add("km_petronad.dashboard_view", KmPetronadDashboard)