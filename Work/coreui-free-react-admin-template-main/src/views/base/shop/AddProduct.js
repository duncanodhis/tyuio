/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from 'react'
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
  CFormSelect,
  CFormInput,
  CFormTextarea,
} from '@coreui/react'
import axios from 'axios'

const AddProduct = () => {
  const [visible, setVisible] = useState(false)
  const [categories, setCategories] = useState([])
  const [packages, setPackages] = useState([])
  const [countries, setCountries] = useState([])
  const [cities, setCities] = useState([])
  const [districts, setDistricts] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedPackage, setSelectedPackage] = useState('')
  const [selectedStockWeight, setSelectedStockWeight] = useState('')
  const [stockPrice, setStockPrice] = useState('')
  const [stockCurrency, setStockCurrency] = useState('GEL')
  const [sellingPrice, setSellingPrice] = useState('')
  const [sellingCurrency, setSellingCurrency] = useState('GEL')
  const [selectedCountry, setSelectedCountry] = useState('')
  const [selectedCity, setSelectedCity] = useState('')
  const [selectedDistrict, setSelectedDistrict] = useState('')
  const [stockPackageDescription, setStockPackageDescription] = useState('')
  const [sellingDescription, setSellingDescription] = useState('')
  const [stockMeasurement, setStockMeasurement] = useState('grams');
 const [sellingMeasurement, setSellingMeasurement] = useState('grams');
 const [ sellingWeight,setSellingWeight] = useState('')

  // Fetch Categories from API
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/categories')
      .then((response) => response.json())
      .then((data) => {
        setCategories(data, setSellingDescription, setStockPackageDescription)
      })
      .catch((error) => console.error('Error fetching categories:', error))
  }, [])
  // Fetch Packages from API based on the selected category
  useEffect(() => {
    if (selectedCategory) {
      fetch(`http://127.0.0.1:5000/api/packages/category/${selectedCategory}`)
        .then((response) => response.json())
        .then((data) => {
          setPackages(data)
        })
        .catch((error) => console.error('Error fetching packages:', error))
    }
  }, [selectedCategory])
  // Fetch Packages weight from API based on the selected package
  useEffect(() => {
    if (selectedPackage) {
      fetch(`http://127.0.0.1:5000/api/packages/${selectedPackage}`)
        .then((response) => response.json())
        .then((data) => {
          setSelectedStockWeight(data)
        })
        .catch((error) => console.error('Error fetching packages:', error))
    }
  }, [selectedPackage])

  useEffect(() => {
    if (selectedPackage) {
      fetch(`http://127.0.0.1:5000/api/packages/${selectedPackage}`)
        .then((response) => response.json())
        .then((data) => {
          setStockPrice(data.price);
          setStockPackageDescription(data.description);
        })
        .catch((error) => console.error('Error fetching package details:', error));
    }
  }, [selectedPackage]);
  // Fetch Countries from API
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/addresses/countries')
      .then((response) => response.json())
      .then((data) => {
        setCountries(data)
      })
      .catch((error) => console.error('Error fetching countries:', error))
  }, [])
 
  // Fetch Cities from API based on the selected country
  useEffect(() => {
    if (selectedCountry) {
      fetch(`http://127.0.0.1:5000/api/countries/${selectedCountry}/cities`)
        .then((response) => response.json())
        .then((data) => {
          setCities(data)
        })
        .catch((error) => console.error('Error fetching cities:', error))
    }
  }, [selectedCountry])
  // Fetch Districts from API based on the selected city
  useEffect(() => {
    if (selectedCity) {
      fetch(
        `http://127.0.0.1:5000/api/countries/${selectedCountry}/cities/${selectedCity}/districts`,
      )
        .then((response) => response.json())
        .then((data) => {
          setDistricts(data)
          console.log(data)
        })
        .catch((error) => console.error('Error fetching districts:', error))
    }
  }, [selectedCity, selectedCountry])
  const handleAddProduct = async (event) => {
    event.preventDefault()
    event.stopPropagation()
    const form = event.currentTarget
    if (form.checkValidity() === false) {
    } else {
      const productData = {
        category: selectedCategory,
        package: selectedPackage,
        package_weight: selectedStockWeight,
        package_measurement:stockMeasurement,
        package_price: stockPrice,
        package_currency: stockCurrency,
        selling_price: sellingPrice,
        selling_currency: sellingCurrency,
        selling_weight: sellingWeight,
        selling_measurement: sellingMeasurement,
        country: selectedCountry,
        city: selectedCity,
        district: selectedDistrict,
        stockPackageDescription: stockPackageDescription,
        sellingDescription: sellingDescription,
      }
      console.log('Product data to be sent:', productData);
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/products', productData, {
          headers: {
            'Content-Type': 'application/json',
          },
        })

        // Handle the response from the server if needed
        console.log('Product data submitted successfully:', response.data)

        // Optionally, you can reset the form fields after successful submission
        setSelectedCategory('')
        setSelectedPackage('')
        setSelectedStockWeight('')
        setStockPrice('')
        setStockCurrency('GEL')
        setSellingPrice('')
        setSellingCurrency('GEL')
        setSelectedCountry('')
        setSelectedCity('')
        setSelectedDistrict('')
        setStockPackageDescription('')
        setSellingDescription('')
        setVisible(false) // Close the modal or hide the form after successful submission
      } catch (error) {
        // Handle any errors that occurred during the API call
        console.error('Error submitting product data:', error)
      }
    }
  }

  return (
    <>
      <CTooltip
        content="Make sure to create 🌱packaging,📌Addresses on the navigation bar 👆 first before adding product"
        placement="right"
      >
        <CButton onClick={() => setVisible(!visible)}>Add Product</CButton>
      </CTooltip>
      <CModal size="lg" alignment="center" visible={visible} onClose={() => setVisible(false)}>
        <CModalHeader>
          <CModalTitle>Add Product</CModalTitle>
        </CModalHeader>
        <CModalBody>
          <CForm className="row g-3">
            <CCol md={6}>
              <CFormSelect
                id="category"
                label="Category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <option>Choose...</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </CFormSelect>
            </CCol>
            <CCol md={6}>
              <CFormSelect
                id="package"
                label="Package/Stock"
                value={selectedPackage}
                onChange={(e) => setSelectedPackage(e.target.value)}
              >
                <option>Choose...</option>
                {packages.map((pack) => (
                  <option key={pack.id} value={pack.id}>
                    {pack.name}
                  </option>
                ))}
              </CFormSelect>
            </CCol>
            <CCol xs={12} md={6}>
              <CFormSelect
                id="weight"
                label="Stock/Package Weight"
                value={selectedStockWeight}
                onChange={(e) => setSelectedStockWeight(e.target.value)}
              >
                <option>Choose...</option>
                {packages.map((pac) => (
                  <option key={pac.id} value={pac.weight}>
                    {pac.weight}
                  </option>
                ))}
              </CFormSelect>
            </CCol>
            <CCol md={6}>
            <CFormSelect
              id="stock-measurement"
              label="Stock Measurement"
              value={stockMeasurement}
              onChange={(e) => setStockMeasurement(e.target.value)}
            > <option value="g">Choose..</option>
              <option value="g">grams</option>
              <option value="mg">milligrams</option>
              <option value="pieces">pieces</option>
            </CFormSelect>
          </CCol>
          <CCol md={6}>
            <CFormSelect
              id="selling-measurement"
              label="Selling Measurement"
              value={sellingMeasurement}
              onChange={(e) => setSellingMeasurement(e.target.value)}
            >
              <option value="g">grams</option>
              <option value="mg">milligrams</option>
              <option value="pieces">pieces</option>
              {/* Add other measurement options as needed */}
            </CFormSelect>
          </CCol>
          <CCol md={6}>
              <CFormInput
                id="selling weight"
                label="selling weight"
                type="number"
                value={sellingWeight}
                onChange={(e) => setSellingWeight(e.target.value)}
                required
              />
            </CCol>
            <CCol xs={12} md={6}>
              <CFormSelect
                id="country"
                label="Country"
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
              >
                <option>Choose...</option>
                {countries.map((country) => (
                  <option key={country} value={country}>
                    {country}
                  </option>
                ))}
              </CFormSelect>
            </CCol>
            <CCol xs={12} md={6}>
              <CFormSelect
                id="city"
                label="City"
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
              >
                <option>Choose...</option>
                {cities.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </CFormSelect>
            </CCol>
            <CCol xs={12} md={6}>
              <CFormSelect
                id="district"
                label="District"
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
              >
                <option>Choose...</option>
                {districts.map((district) => (
                  <option key={district} value={district}>
                    {district}
                  </option>
                ))}
              </CFormSelect>
            </CCol>
            <CCol md={6}>
              <CFormSelect
                id="stock-currency"
                label="Stock Currency"
                value={stockCurrency}
                onChange={(e) => setStockCurrency(e.target.value)}
              >
                <option value="GEL">GEL</option>
                <option value="EUR">EUR</option>
              </CFormSelect>
            </CCol>
            <CCol md={6}>
              <CFormInput
                id="stock-price"
                label="Stock Price"
                type="number"
                value={stockPrice}
                onChange={(e) => setStockPrice(e.target.value)}
                required
              />
            </CCol>
            <CCol md={6}>
              <CFormSelect
                id="selling-currency"
                label="Selling Currency"
                value={sellingCurrency}
                onChange={(e) => setSellingCurrency(e.target.value)}
              >
                <option value="GEL">GEL</option>
                <option value="EUR">EUR</option>
                
                {/* Add other currency options as needed */}
              </CFormSelect>
            </CCol>
            <CCol md={6}>
              <CFormInput
                id="selling-price"
                label="Selling Price"
                type="number"
                value={sellingPrice}
                onChange={(e) => setSellingPrice(e.target.value)}
                required
              />
            </CCol>
            <CCol xs={12} md={12}>
              <CFormTextarea
                id="stock-description"
                label="Stock Description"
                rows={3}
                value={stockPackageDescription}
                onChange={(e) => setStockPackageDescription(e.target.value)}
              />
            </CCol>
            <CCol xs={12} md={12}>
              <CFormTextarea
                id="selling-description"
                label="Selling Description"
                rows={3}
                value={sellingDescription}
                onChange={(e) => setSellingDescription(e.target.value)}
              />
            </CCol>
          </CForm>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setVisible(false)}>
            Close
          </CButton>
          <CTooltip
            content="Stock price is the same as package price, so you have to input the selling price for the clients to see"
            placement="right"
          >
            <CButton color="primary" onClick={handleAddProduct}>
              Save changes
            </CButton>
          </CTooltip>
        </CModalFooter>
      </CModal>
    </>
  )
}

export default AddProduct
