import React from 'react'
import { NavLink } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import {
  CContainer,
  CHeader,
  CHeaderBrand,
  CHeaderDivider,
  CHeaderNav,
  CHeaderToggler,
  CNavLink,
  CNavItem,
  CCollapse,
  CDropdownMenu,
  CNavbarNav,
  CDropdown,
  CDropdownToggle,
  CDropdownItem,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilMenu } from '@coreui/icons'
import { AppBreadcrumb } from './index'
import { AppHeaderDropdown } from './header/index'
import { logo } from 'src/assets/brand/logo'

const AppHeader = () => {
  const dispatch = useDispatch()
  const sidebarShow = useSelector((state) => state.sidebarShow)

  return (
    <CHeader position="sticky" className="mb-4">
      <CContainer fluid>
        <CHeaderToggler
          className="ps-1"
          onClick={() => dispatch({ type: 'set', sidebarShow: !sidebarShow })}
        >
          <CIcon icon={cilMenu} size="lg" />
        </CHeaderToggler>
        <CHeaderBrand className="mx-auto d-md-none" to="/">
          <CIcon icon={logo} height={48} alt="Logo" />
        </CHeaderBrand>
        <CHeaderNav className="d-none d-md-flex me-auto">
          <CNavItem>
            <CNavLink to="/dashboard" component={NavLink}>
              Dashboard
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CCollapse className="navbar-collapse" visible={true}>
              <CNavbarNav>
                <CDropdown dark component="li" variant="nav-item">
                  <CDropdownToggle>
                    <span role="img" aria-label="Addresses">
                      📌
                    </span>{' '}
                    Addresses
                  </CDropdownToggle>
                  <CDropdownMenu>
                    <CDropdownItem>
                      <CNavLink to="/base/addresses" component={NavLink}>
                        Create Address
                      </CNavLink>
                    </CDropdownItem>
                    <CDropdownItem>
                      <CNavLink to="/base/addresses" component={NavLink}>
                        See addresses
                      </CNavLink>
                    </CDropdownItem>
                  </CDropdownMenu>
                </CDropdown>
              </CNavbarNav>
            </CCollapse>
          </CNavItem>
          <CNavItem>
            <CCollapse className="navbar-collapse" visible={true}>
              <CNavbarNav>
                <CDropdown dark component="li" variant="nav-item">
                  <CDropdownToggle>
                    <span role="img" aria-label="Packaging">
                      🌱
                    </span>{' '}
                    Packaging
                  </CDropdownToggle>
                  <CDropdownMenu>
                    <CDropdownItem>
                      <CNavLink to="/base/category" component={NavLink}>
                        Create Category
                      </CNavLink>
                    </CDropdownItem>
                    <CDropdownItem>
                      <CNavLink to="/base/addPackage" component={NavLink}>
                        Add Packaging
                      </CNavLink>
                    </CDropdownItem>
                  </CDropdownMenu>
                </CDropdown>
              </CNavbarNav>
            </CCollapse>
          </CNavItem>
          <CNavItem>
            <CNavLink href="#">
              <span role="img" aria-label="Monitoring">
                👁️
              </span>{' '}
              Monitoring
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CNavLink href="#">
              <span role="img" aria-label="Casino">
                🎰
              </span>{' '}
              Casino
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CNavLink href="#">
              <span role="img" aria-label="Settings">
                ⚙️
              </span>{' '}
              Settings
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CNavLink href="#">
              <span role="img" aria-label="Rent">
                🏠
              </span>{' '}
              Rent
            </CNavLink>
          </CNavItem>
        </CHeaderNav>
        <CHeaderNav className="ms-3">
          <AppHeaderDropdown />
        </CHeaderNav>
      </CContainer>
      <CHeaderDivider />
      <CContainer fluid>
        <AppBreadcrumb />
      </CContainer>
    </CHeader>
  )
}

export default AppHeader
