import axios from 'axios';
import store from '../store/index';

const baseURL = 'http://127.0.0.1:8000'
const AUTH_API = axios.create({
    baseURL: baseURL,// Adres do serwera Django
    timeout: 5000,
    headers: {
        Authorization: localStorage.getItem('token')
            ? 'JWT ' + localStorage.getItem('token')
            : null,
            'Content-Type': 'application/json',
            accept: 'application/json',
    },
})

AUTH_API.interceptors.response.use(
	(response) => {
		return response;
	},
	async function (error) {
		const originalRequest = error.config;

		if (typeof error.response === 'undefined') {
			alert(
				'A server/network error occurred. ' +
					'Looks like CORS might be the problem. ' +
					'Sorry about this - we will get it fixed shortly.'
			);
			return Promise.reject(error);
		}

		if(error.response.status === 401 && error.response.data.detail === 'Token contained no recognizable user identification'){
			alert('Niepoprawny token')
			return Promise.reject(error);
		}

		if (
			error.response.status === 401 &&
			originalRequest.url === '/api/v1/token/refresh/'
		) {
			if(error.response.data.detail === 'Twoje Hasło zostało przed chwilą zmienione, proszę zalogować się ponownie.'){
				console.log(error.response.data.detail)
				alert('Twoje hasło niedawno zostało zmienione, zaloguj się ponownie.')
				return Promise.reject(error);
			}
			else{
				// window.location.href = 'http://localhost:8080/login';
				console.log(error.response.data.detail+'tutaj alert po promise.reject')
				alert('Token się wysypał, zaloguj się ponownie')
				return Promise.reject(error);
			}
		}

		if (
			error.response.status === 403
		) {
			// window.location.href = 'http://localhost:8080/login';
            alert('Twoje hasło niedawno zostało zmienione, zaloguj się ponownie.')
			return Promise.reject(error);
		}

		if (
			(error.response.data.code === 'token_not_valid' || error.response.data.detail === 'Authentication credentials were not provided.') &&
			originalRequest.url !== '/api/v1/token/verify/' &&
			error.response.status === 401 &&
			error.response.statusText === 'Unauthorized'
		) {
			const refreshToken = localStorage.getItem('refreshToken');

			try{
				if (refreshToken) {
					console.log('tal')
					const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));
	
					// exp date in token is expressed in seconds, while now() returns milliseconds:
					const now = Math.ceil(Date.now() / 1000);
					console.log(tokenParts.exp);
					console.log(originalRequest)
	
					if (tokenParts.exp > now) {
						return AUTH_API
							.post('/api/v1/token/refresh/', { refresh: localStorage.getItem('refreshToken') })
							.then((response) => {
								// localStorage.setItem( 'token', response.data.access );
								// localStorage.setItem( 'refreshToken', response.data.refresh );
								store.commit('setToken', {
									access: response.data.access,
									refresh: response.data.refresh
								})
	
								AUTH_API.defaults.headers['Authorization'] =
									'JWT ' + response.data.access;
								originalRequest.headers['Authorization'] =
									'JWT ' + response.data.access;
	
								return AUTH_API(originalRequest);
							})
							.catch((err) => {
								console.log('tutaj error z auth api po wyjenaiu sie')
								return Promise.reject(error);
							});
					} else {
						alert('Refresh token is expired', tokenParts.exp, now);
						// window.location.href = 'http://localhost:8080/login';
					}
				} else {
					console.log('Refresh token not available.');
					// window.location.href = 'http://localhost:8080/login';
				}
			}catch( error ){
				alert(error)
				// return
			}
		}
		console.log('a')
		// specific error handling done elsewhere
		return Promise.reject(error);
	}
);

export {AUTH_API}
