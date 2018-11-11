import { Vue } from '../../vue.js'

import getParameterByName from '../../core/getParameterByName'
import updateQueryString from '../../core/updateQueryString'
import removeQueryParameter from '../../core/removeQueryParameter';


var catalog = new Vue({
    name: 'catalog',
    el: '#catalog',
    data: {
        sortingOption: 'scoring',
        sortingDirection: 'descending',
    },
    created() {
        let parsedOption = getParameterByName('o');
        let parsedDirection = getParameterByName('dir');
        if ( parsedOption !== null ) {
            this.sortingOption = parsedOption;
        }
        if ( parsedDirection !== null ) {
            this.sortingDirection = parsedDirection;
        }
    },
    methods: {
        setActiveOption(option) {
            this.sortingOption = option;
            this.sortingRedirect();
        },
        toggleSortingDirection() {
            if (this.sortingDirection === 'descending') {
                this.sortingDirection = 'ascending';
            } else {
                this.sortingDirection = 'descending';
            }
            this.sortingRedirect();
        },
        sortingRedirect() {
            let currentQuery = location.search;
            currentQuery = updateQueryString(currentQuery, 'o', this.sortingOption);
            currentQuery = updateQueryString(currentQuery, 'dir', this.sortingDirection);
            currentQuery = removeQueryParameter(currentQuery, 'page');
            document.location.search = currentQuery;
        }
    }
});

