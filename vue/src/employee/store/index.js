import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    role: null,
    name: "",
    last_name: "",
    employee_id: null,
    accessToken: localStorage.getItem("employeeToken"),
    refreshToken: localStorage.getItem("employeeRefreshToken"),
    isAuthenticated: false,
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
    setRole(state, data){
      state.role = data.role;
      state.name = data.name;
      state.last_name = data.last_name;
      state.employee_id = data.employee_id;
    },
    setToken (state, { access, refresh }) {
      localStorage.setItem( 'employeeToken', access );
      localStorage.setItem( 'employeeRefreshToken', refresh );
      state.accessToken = access
      state.refreshToken = refresh
    },

    setRefreshToken (state){
      state.refreshToken = localStorage.getItem('employeeRefreshToken')
    },

    userLogout (state){
      if(state.isAuthenticated){
        if(localStorage.getItem("employeeToken")){
          localStorage.removeItem("employeeToken")
        }
        localStorage.removeItem("employeeRefreshToken")
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
})