// javascript functionality for nav dropdown menu
const trigger = document.getElementById('dropdownTrigger')
const dropdown = document.getElementById('dropdownList')
let isOpen = false

const toggleActive = (el) => {
	el.classList.toggle('active')
}

const closeDropdown = () => {
	dropdown.style.display = 'none'
	isOpen = false
}

trigger.addEventListener('click', () => {
	if (isOpen) {
		closeDropdown()
	} else {
		dropdown.style.display = 'flex'
		isOpen = true
	}
	toggleActive(trigger)
})

dropdown.addEventListener('click', () => {
	toggleActive(trigger)
})

document.addEventListener('click', (e) => {
	const target = e.target

	if (!trigger.contains(target) && !dropdown.contains(target)) {
		closeDropdown()

		if (trigger.classList.contains('active')) {
			toggleActive(trigger)
		}
	}
})

// javascript functionality for dialogs/modals
const openPostModal = document.querySelector('[data-open-post-modal]')
const postModal = document.querySelector('[data-post-modal]')

openPostModal.addEventListener('click', () => {
	postModal.showModal()
})

postModal.addEventListener('click', (e) => {
	const dimensions = postModal.getBoundingClientRect()
	if (
		e.clientX < dimensions.left ||
		e.clientX > dimensions.right ||
		e.clientY < dimensions.top ||
		e.clientY > dimensions.bottom
	) {
		postModal.close()
	}
})
