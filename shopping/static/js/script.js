/**
 * Remove alert message after 5 seconds from the DOM.
 */
document.addEventListener('DOMContentLoaded', function () {
    const alert = document.querySelector('[data-alert]');
    if (alert) {
        setTimeout(function () {
            alert.style.display = 'none';
        }, 5000);
    }
}, false);

/**
 * Set color for SVG icon in the popup modal.
 *
 * @param {boolean} green - Whether to set the color to green or red
 */
function changeIconColor(green = true) {
    const svg = document.getElementById('svgPopupIcon');
    if (green) {
        svg.classList.remove('text-red-400', 'dark:text-red-400');
        svg.classList.add('text-green-400', 'dark:text-green-400');
    } else {
        svg.classList.remove('text-green-400', 'dark:text-green-400');
        svg.classList.add('text-red-400', 'dark:text-red-400');
    }
}

/**
 * Reset form fields when user clicks on the reset button
 *
 * @param {string} formId
 */
function resetForm(formId) {
    document.getElementById(formId).reset();
}

/**
 * Make a prototype of the String object to capitalize the first letter of a string.
 */
Object.defineProperty(String.prototype, 'capitalize', {
    value: function () {
        return this.charAt(0).toUpperCase() + this.slice(1);
    },
    enumerable: false
});

/**
 * Add or remove error message based on the condition
 * @param {string} id - The id of the error message
 * @param {boolean} condition - The condition to check
 * @param {boolean} submit - Whether to prevent the form submission
 */
function addRemoveError(id, condition, submit = true) {
    if (condition) {
        submit && event.preventDefault();
        document.getElementById(id).classList.add('active');
    } else {
        document.getElementById(id).classList.remove('active');
    }
};

/**
 * Show or hide validation messages for the form fields.
 *
 * @param {HTMLFormElement} form
 * @param {string[]} formFields
 */
function showHideValidationMessages(form, formFields) {
    formFields.forEach(id => {
        const input = document.getElementById(id);
        form.addEventListener('submit', (event) => {
            addRemoveError(`${id}Error`, input.validity.valueMissing || input.validity.tooShort, true)
        });
        input.addEventListener('input', () => addRemoveError(`${id}Error`, input.validity.valueMissing || input.validity.tooShort, false));
    });
}

function setResourceIdAndType(button) {
    document.getElementById('resourceIdAndType').value = JSON.stringify({ resourceId: button.dataset.resourceId, type: button.dataset.type });
}

/* Variables that hold the old state of resource name and description. */
let oldName = '';
let oldDescription = '';

/**
* Update resource
*
* @param {HTMLElement} element - the button element
* @param {boolean} update - if true, update the resource
*
* @returns {void}
*/
function updateResource(element, update = false) {
    const afterActionMessageInPopupModal = document.getElementById('afterActionMessageInPopupModal');
    const row = element.closest('tr');

    element.style.display = 'none'
    element.nextElementSibling.style.display = 'block';

    const id = element.dataset.resourceId;
    const resourceType = element.dataset.type;
    const name = row.querySelector('td:nth-child(3) div').innerText;
    const description = row.querySelector('td:nth-child(4) div')


    if (!update) {
        oldName = name;
        oldDescription = description.innerText;
    }

    !update && description.focus();

    if (update) {
        fetch(`/${resourceType}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                description: description.innerText
            })
        })
            .then(response => {
                if (response.status === 200) {
                    changeIconColor();
                    afterActionMessageInPopupModal.innerText = `${resourceType.capitalize()} updated successfully.`;
                } else {
                    name.innerText = oldName;
                    description.innerText = oldDescription;
                    changeIconColor(false);
                    afterActionMessageInPopupModal.innerText = `${resourceType.capitalize()} cannot be updated.`;
                }
                const button = document.getElementById('showHidePopupModal');
                button.click();
                element.previousElementSibling.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

/**
 * Remove resource
 *
 * @returns {void}
 */
function removeResource() {
    const resourceData = document.getElementById('resourceIdAndType').value;
    const id = JSON.parse(resourceData).resourceId;
    const resourceType = JSON.parse(resourceData).type;

    const button = document.querySelector(`[data-resource-id="${id}"]`);
    row = button.closest('tr');

    fetch(`/${resourceType}/${id}`, {
        method: 'DELETE'
    })
        .then(response => {
            if (response.status === 200) {
                afterActionMessageInPopupModal.innerText = `${resourceType.capitalize()} deleted successfully.`;
                changeIconColor();
                row.remove();
            } else {
                changeIconColor(false);
                const message = `${resourceType.capitalize()} cannot be deleted. There are records associated with this ${resourceType}.`;
                document.getElementById('resourceCantBeDeletedMessage').value = message;
                afterActionMessageInPopupModal.innerText = message;
            }
            const button = document.getElementById('showHidePopupModal');
            button.click();
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// Path: shopping/static/js/script.js