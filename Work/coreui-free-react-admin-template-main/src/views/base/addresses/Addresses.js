/* eslint-disable prettier/prettier */
import React, { useState } from 'react';
import axios from 'axios';
import {
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CCollapse,
  CForm,
  CFormLabel,
  CFormFeedback,
  CButton,
  CRow,
} from '@coreui/react';

const Address = () => {
  const [locations, setLocations] = useState([]);
  const [newLocation, setNewLocation] = useState({});
  const [isOpen, setIsOpen] = useState(false);
  const [validated, setValidated] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    event.stopPropagation();

    const form = event.currentTarget;
      if (form.checkValidity() === false) {
        setValidated(true);
      } else {
        try {
          const formData = new FormData();
          formData.append('country', newLocation.country);
          formData.append('city', newLocation.city);
          formData.append('district', newLocation.district);
          formData.append('cityImage', newLocation.cityImage);
          formData.append('districtImage', newLocation.districtImage);

          const response = await axios.post('http://127.0.0.1:5000/api/addresses', formData, {
            headers: {
              'Content-Type': 'multipart/form-data', // Set the correct content type for file uploads
            },
          });

          const location = {
            ...response.data,
            cityImage: URL.createObjectURL(newLocation.cityImage),
            districtImage: URL.createObjectURL(newLocation.districtImage),
          };

          setLocations([...locations, location]);
          setNewLocation({});
          setValidated(false);
        } catch (error) {
          console.error('Error creating location:', error);
        }
      }
    };

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleCityImageChange = (e) => {
    const file = e.target.files[0];
    setNewLocation({ ...newLocation, cityImage: file });
  };

  const handleDistrictImageChange = (e) => {
    const file = e.target.files[0];
    setNewLocation({ ...newLocation, districtImage: file });
  };

  return (
    <div>
      <CCard>
        <CCardHeader>Create Location</CCardHeader>
        <CCardBody>
          <CForm
            className="row g-3 needs-validation"
            noValidate
            validated={validated}
            onSubmit={handleSubmit}
          >
            <CRow>
              <CCol md={6}>
                <CFormLabel htmlFor="country">Country</CFormLabel>
                <input
                  id="country"
                  required
                  className="form-control"
                  value={newLocation.country || ''}
                  onChange={(e) => setNewLocation({ ...newLocation, country: e.target.value })}
                />
                <CFormFeedback>Please provide a country.</CFormFeedback>
              </CCol>
              <CCol md={6}>
                <CFormLabel htmlFor="city">City</CFormLabel>
                <input
                  id="city"
                  required
                  className="form-control"
                  value={newLocation.city || ''}
                  onChange={(e) => setNewLocation({ ...newLocation, city: e.target.value })}
                />
                <CFormFeedback>Please provide a city.</CFormFeedback>
              </CCol>
            </CRow>
            <CRow>
              <CCol md={6}>
                <CFormLabel htmlFor="district">District</CFormLabel>
                <input
                  id="district"
                  required
                  className="form-control"
                  value={newLocation.district || ''}
                  onChange={(e) => setNewLocation({ ...newLocation, district: e.target.value })}
                />
                <CFormFeedback>Please provide a district.</CFormFeedback>
              </CCol>
              <CCol md={6}>
                <CFormLabel htmlFor="cityImage">City Image</CFormLabel>
                <input type="file" id="cityImage" onChange={handleCityImageChange} />
              </CCol>
            </CRow>
            <CRow>
              <CCol md={6}>
                <CFormLabel htmlFor="districtImage">District Image</CFormLabel>
                <input type="file" id="districtImage" onChange={handleDistrictImageChange} />
              </CCol>
              <CCol md={6}>
                <CButton color="primary" type="submit">
                  Create
                </CButton>
              </CCol>
            </CRow>
          </CForm>
        </CCardBody>
      </CCard>

      <CCard>
        <CCardHeader onClick={handleToggle}>Show Available Addresses</CCardHeader>
        <CCollapse show={isOpen}>
          <CCardBody>
            {locations.map((location) => (
              <div key={location.id}>
                <h5>Country: {location.country}</h5>
                <h5>City: {location.city}</h5>
                <h5>District: {location.district}</h5>
                {location.city_image && <img src={location.city_image} alt={location.city} />}
                {location.district_image && (
                  <img src={location.district_image} alt={location.district} />
                )}
              </div>
            ))}
          </CCardBody>
        </CCollapse>
      </CCard>
    </div>
  );
};

export default Address;
