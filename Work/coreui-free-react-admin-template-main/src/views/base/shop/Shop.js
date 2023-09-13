import React from 'react'
import { CCard, CCardBody, CCardGroup, CCol, CContainer, CRow } from '@coreui/react'
import AddProduct from './AddProduct'
import Order from './Order'
import Token from './Token'
const Shop = () => {
  return (
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={12}>
            <CCardGroup>
              <CCard className="p-6">
                <CCardBody>
                  <CRow className="mb-3">
                    <CCol md={8}>
                      <AddProduct />
                    </CCol>
                    <CCol md={4}>
                      <Token />
                    </CCol>
                  </CRow>
                  <div className="row g-5">
                    <Order />
                  </div>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Shop
