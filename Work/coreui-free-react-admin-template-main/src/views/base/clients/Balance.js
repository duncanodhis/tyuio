/* eslint-disable prettier/prettier */
import React, { useState } from 'react'
import {
  CButton,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CTooltip,
  CForm,
  CCol,
  CFormInput,
} from '@coreui/react'

const Balance = () => {
  const [visible, setVisible] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedStock, setSelectedStock] = useState(null)
  const [sellingPrice, setSellingPrice] = useState('')
  const [sellingDescription, setSellingDescription] = useState('')
  const [selectedCountry, setSelectedCountry] = useState('')
  const [selectedCity, setSelectedCity] = useState('')
  const [selectedDistrict, setSelectedDistrict] = useState('')

  const handleBalance = () => {
    // Perform actions when the "Save changes" button is clicked
    // You can access the selected values and perform further actions here
    console.log(selectedCategory)
    console.log(setSelectedCategory)
    console.log(selectedStock)
    console.log(setSelectedStock)
    console.log(sellingPrice)
    console.log(setSellingPrice)
    console.log(sellingDescription)
    console.log(setSellingDescription)
    console.log(selectedCountry)
    console.log(setSelectedCountry)
    console.log(selectedCity)
    console.log(setSelectedCity)
    console.log(selectedDistrict)
    console.log(setSelectedDistrict)
    setVisible(false)
  }

  return (
    <>
      <CTooltip
        content=""
        placement="right"
      >
        <CButton onClick={() => setVisible(!visible)}>balance</CButton>
      </CTooltip>
      <CModal alignment="center" visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>balance</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CForm className="row g-3">
            <CCol xs={12} md={12}>
            <CFormInput type="text" placeholder="Default input" aria-label="default input example"/>
            </CCol>
            <CCol xs={12} md={12}>
            <CFormInput type="text" placeholder="Default input" aria-label="default input example"/>
            <CButton color="primary" onClick={handleBalance }>
              Add
            </CButton>
            <CModalHeader>
                 <CModalTitle>Take away</CModalTitle>
            </CModalHeader>
            <CFormInput type="text" placeholder="Default input" aria-label="default input example"/>
            <CButton color="primary" onClick={handleBalance }>
              Take away
            </CButton>
            </CCol>
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setVisible(false)}>
            Close
          </CButton>
          <CTooltip
            content=""
            placement="right"
          >
            <CButton color="primary" onClick={handleBalance }>
              Save changes
            </CButton>
          </CTooltip>
        </CModalFooter>
      </CModal>
    </>
  )
}

export default Balance
