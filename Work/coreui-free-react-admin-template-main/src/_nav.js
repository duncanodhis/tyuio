import React from 'react'
import CIcon from '@coreui/icons-react'
import {
  cilFrown,
  cilChatBubble,
  cilBalanceScale,
  cilEnvelopeOpen,
  cilSpeedometer,
  cilFunctionsAlt,
  cilBuilding,
  cilCart,
  cilPeople,
  cilCreditCard,
  cilTruck,
} from '@coreui/icons'
import { CNavGroup, CNavItem } from '@coreui/react'

const _nav = [
  {
    component: CNavItem,
    name: 'Dashboard',
    to: '/dashboard',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
    badge: {
      color: 'info',
    },
  },
  {
    component: CNavGroup,
    name: 'Section 1',
    items: [
      {
        component: CNavItem,
        name: 'Shop',
        to: '/base/shop',
        icon: <CIcon icon={cilBuilding} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Goods',
        to: '/base/goods',
        icon: <CIcon icon={cilCart} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Clients',
        to: '/base/clients',
        icon: <CIcon icon={cilPeople} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Wallets',
        to: '/base/wallets',
        icon: <CIcon icon={cilCreditCard} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Couriers',
        to: '/base/courier',
        icon: <CIcon icon={cilTruck} customClassName="nav-icon" />,
      },
    ],
  },
  {
    component: CNavGroup,
    name: 'Section 2',
    items: [
      {
        component: CNavItem,
        name: 'NewsLetter',
        to: '/base/newsletter',
        icon: <CIcon icon={cilEnvelopeOpen} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Discount',
        to: '/base/discount',
        icon: <CIcon icon={cilBalanceScale} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Statistics',
        to: '/charts',
        icon: <CIcon icon={cilFunctionsAlt} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Review',
        to: '/base/review',
        icon: <CIcon icon={cilChatBubble} customClassName="nav-icon" />,
      },
      {
        component: CNavItem,
        name: 'Dispute',
        to: '/base/disputes',
        icon: <CIcon icon={cilFrown} customClassName="nav-icon" />,
      },
    ],
  },
]

export default _nav
