import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    role: null,
    accessToken: localStorage.getItem("clientToken"),
    refreshToken: localStorage.getItem("clientRefreshToken"),
    isAuthenticated: false,
    allBusinessActivities: [],
    distinctServices: [],
    distinctEmployeeSpecs: [],
    countries: [
      {
        label: 'Polska',
        phone: '+48',
        countryCode: "PL",
        rule: [
          v => {return(v.length == 0 || v.length <= 9) || 'Błędny nr telefonu'},
          v => {return(v.length == 0 || /\d{3}[ -]?\d{3}[ -]?\d{3}/.test(v)) || 'Błędny nr telefonu'},
        ],
      },
      {
        label: 'Niemcy',
        phone: '+49',
        countryCode: "DE",
        rule: [
          v => {return(v.length == 0 || (v.length >= 2 && v.length <= 12)) || 'Falsche Telefonnummer'},
          v => {return(v.length == 0 || /\d{3}[ -]?\d{3}[ -]?\d{3}/.test(v)) || 'Falsche Telefonnummer'},
        ],
      },
      {
        label: 'Wielka Brytania',
        phone: '+44',
        countryCode: "GB",
        rule: [
          v => {return(v.length == 0 || /\d{3}[ -]?\d{3}[ -]?\d{3}/.test(v)) || 'Wrong phone number'},
        ],
      }
    ],
    rules: {
      emailRules: [
        v => !!v || 'E-mail jest wymagany',
        v => /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v)
          || 'E-mail musi być poprawny przykład:\n example@mail.com',
      ],
      userNameRules: [
        v => !!v || 'Nazwa użytkownika jest wymagana',
      ],
      nameRules: [
        v => !!v || 'Imię jest wymagane',
        v => (v && v.length >= 3) || 'Imię musi zawierać co najmniej 3 znaki',
        v => /^[a-zA-ZżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$/.test(v) || 'Imię może zawierać jedynie litery',
      ],
      lastNameRules: [
        v => !!v || 'Nazwisko jest wymagane',
        v => (v && v.length >= 3) || 'Nazwisko musi zawierać co najmniej 3 znaki',
        v => /^[a-zA-ZżźćńółęąśŻŹĆĄŚĘŁÓŃ\s-]*$/.test(v) || 'Nazwisko może zawierać jedynie litery',
      ],
      onlyLetters: [
        v => !!v || 'Pole wymagane',
        v => (v && v.length >= 2) || 'Pole musi zawierać co najmniej 2 znaki',
        v => /^[a-zA-ZżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$/.test(v) || 'Pole może zawierać jedynie litery',
      ],
      onlyNumbers: [
        v => !!v || 'Pole wymagane',
        v => /^[0-9]*$/.test(v) || 'Pole może zawierać jedynie cyfry',
      ],
      postcode: [
        v => /\d{2}-\d{3}$/.test(v) || 'Nie właściwy format kodu pocztowego',
      ],
      numbersLetters: [
        v => /^[0-9a-zA-ZżźćńółęąśŻŹĆĄŚĘŁÓŃ]*$/.test(v) || 'Pole nie może zawierać znaków specjalnych',
      ],
      required: [
        v => !!v || 'Pole wymagane',
      ],
    },
  },
  mutations: {
    setBusinessActivities(state, value){
      state.allBusinessActivities = value
    },
    setDistinctEmployeeSpecs(state, value){
      state.distinctEmployeeSpecs = value
    },
    setDistinctServices(state, value){
      state.distinctServices = value
    },
    setRole(state, value){
      state.role = value
    },
    async setToken (state, { access, refresh }) {
      localStorage.setItem( 'clientToken', access );
      localStorage.setItem( 'clientRefreshToken', refresh );
      state.accessToken = access
      state.refreshToken = refresh
    },

    setRefreshToken (state){
      state.refreshToken = localStorage.getItem('clientRefreshToken')
    },

    userLogout (state){
      if(state.isAuthenticated){
        if(localStorage.getItem("clientToken")){
          localStorage.removeItem("clientToken")
        }
        localStorage.removeItem("clientRefreshToken")
        state.accessToken = null
        state.refreshToken = null
        state.isAuthenticated = false;
      }
    },

    setIsAuthenticated (state, value){
      state.isAuthenticated = value
    },

    destroyToken (state) {
      state.accessToken = null
      state.refreshToken = null
      state.isAuthenticated = false;
    },

  },
  actions: {
    async getBusinessActivitesAndServices({commit}){
      await axios.get('http://127.0.0.1:8000/api/v1/client/businessactivities/')
      .then(res => {
        commit("setBusinessActivities", res.data.business_activity)
        commit("setDistinctServices", res.data.distinct_services)
        commit("setDistinctEmployeeSpecs", res.data.distinct_employee_specs)
      })
    }
  },
})