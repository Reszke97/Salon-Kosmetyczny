import Vue from 'vue'
import Vuex from 'vuex'
import { AUTH_API } from '../authorization/AuthAPI'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    role: null,
    test: false,
    accessToken: localStorage.getItem("employeeToken"),
    refreshToken: localStorage.getItem("employeeRefreshToken"),
    isAuthenticated: false,
    isEditing: false,
    dealerChosen: false,
    basketPositionIndex: null,
    dealerDialog: false,
    installationDialog: false,
    info: false,
    userQuoteID: null,
    countries: [
      {
        // link: 'https://github.com/lipis/flag-icons/blob/main/flags/4x3/pl.svg',
        label: 'Polska',
        phone: '+48',
        countryCode: "PL",
        rule: [
          v => {return(v.length == 0 || v.length <= 9) || 'Błędny nr telefonu'},
          v => {return(v.length == 0 || /\d{3}[ -]?\d{3}[ -]?\d{3}/.test(v)) || 'Błędny nr telefonu'},
        ],
      },
      {
        // link: 'https://github.com/lipis/flag-icons/blob/main/flags/4x3/de.svg',
        label: 'Niemcy',
        phone: '+49',
        countryCode: "DE",
        rule: [
          v => {return(v.length == 0 || (v.length >= 2 && v.length <= 12)) || 'Falsche Telefonnummer'},
          v => {return(v.length == 0 || /\d{3}[ -]?\d{3}[ -]?\d{3}/.test(v)) || 'Falsche Telefonnummer'},
        ],
      },
      {
        // link: 'https://github.com/lipis/flag-icons/blob/main/flags/4x3/gb.svg',
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
  getters: {
    totalSumToPay(state) {
      return state.basket.reduce((sum, item) => {
        sum += (item.getters.totalPrice * item.chosenConfiguration.windowFeatures.quantity);
        return sum
      }, 0)
    },
  },
  mutations: {
    setRole(state, value){
      state.role = value
    },
    setUserQuoteID(state, value){
      state.userQuoteID = value
    },
    clearBasket(state){
      state.basket = [...basketTestData]
    },
    setInfo(state){
      state.info = !state.info
    },
    setIsEditing(state, value){
      state.isEditing = value
    },
    setInstallationDialog(state){
      state.installationDialog = !state.installationDialog
    },
    setDealerDialog(state){
      state.dealerDialog = !state.dealerDialog
    },
    setBasketPositionIndex(state, index){
      state.basketPositionIndex = index
    },
    setBasket(state, object){
      state.basket.push(object);
    },
    deleteDataFromBasket(state, index){
      state.basket.splice(index, 1)
    },
    copyDataToBasket(state, index){
      state.basket.push(state.basket[index])
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
      state.authenticated = false;
    },

  },
  actions: {
    async editBasket({state, commit}, object){
      state.basket.splice(state.basketPositionIndex, 1, object)
      commit("setIsEditing")
    },
  },
  // modules: {
  //   configuration
  // }
})