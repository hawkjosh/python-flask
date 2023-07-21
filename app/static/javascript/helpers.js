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

// javascript functionality for new comments
const newCommentOpen = document.querySelector('[data-new-comment-open]')
const newCommentClose = document.querySelector('[data-new-comment-close]')
const newComment = document.querySelector('[data-new-comment]')
const newCommentText = document.querySelector('[data-new-comment-text]')

const clearCommentText = () => {
	newCommentText.value = ''
}

newCommentOpen.addEventListener('click', () => {
	document.body.classList.add('no-scroll')
	newComment.showModal()
})

newCommentClose.addEventListener('click', () => {
	clearCommentText()
	document.body.classList.remove('no-scroll')
	newComment.close()
})

// newComment.addEventListener('click', (e) => {
// 	const dimensions = newComment.getBoundingClientRect()
// 	if (
// 		e.clientX < dimensions.left ||
// 		e.clientX > dimensions.right ||
// 		e.clientY < dimensions.top ||
// 		e.clientY > dimensions.bottom
// 	) {
// 		newComment.close()
// 	}
// })

// javascript functionality for comment reply
document.addEventListener('DOMContentLoaded', () => {
	const commentReplyOpenBtns = document.querySelectorAll(
		'[data-comment-reply-open]'
	)
	const commentReplyClose = document.querySelector('[data-comment-reply-close]')
	const commentReply = document.querySelector('[data-comment-reply]')
	const commentReplyText = document.querySelector('[data-comment-reply-text]')
	const commentReplyComment = document.querySelector(
		'[data-comment-reply-comment]'
	)
	const commentReplyUsername = document.querySelector(
		'[data-comment-reply-username]'
	)
	const commentReplyDate = document.querySelector('[data-comment-reply-date]')
	let scrollPosition = 0

	const clearReplyText = () => {
		commentReplyText.value = ''
	}

	const closeModal = () => {
		clearReplyText()
		document.body.classList.remove('no-scroll')
		commentReply.close()
		window.scrollTo(0, scrollPosition)
	}

	commentReplyOpenBtns.forEach((btn) => {
		btn.addEventListener('click', () => {
			scrollPosition = window.scrollY
			const commentId = btn.getAttribute('data-comment-reply-open')
			const commentCard = document.querySelector(
				`[data-comment-id="${commentId}"]`
			)
			const comment = commentCard.getAttribute('data-comment-content')
			const username = commentCard.getAttribute('data-comment-username')
			const date = commentCard.getAttribute('data-comment-date')
			const form = commentReply.querySelector('form')
			commentReplyComment.textContent = comment
			commentReplyUsername.textContent = username
			commentReplyDate.textContent = date
			form.action = `/comment/reply/${commentId}`
			document.body.classList.add('no-scroll')
			commentReply.showModal()
		})
	})

	commentReplyClose.addEventListener('click', () => {
		closeModal()
	})
})

// javascript functionality for comment edit
const commentEditOpenBtns = document.querySelectorAll(
	'[data-comment-edit-open]'
)
const commentEditClose = document.querySelector('[data-comment-edit-close]')
const commentEdit = document.querySelector('[data-comment-edit]')
const commentEditComment = document.querySelector('[data-comment-edit-comment]')
let scrollPosition = 0

const closeModal = () => {
	document.body.classList.remove('no-scroll')
	commentEdit.close()
	window.scrollTo(0, scrollPosition)
}

commentEditOpenBtns.forEach((btn) => {
	btn.addEventListener('click', () => {
		scrollPosition = window.scrollY
		const commentId = btn.getAttribute('data-comment-edit-open')
		const commentCard = document.querySelector(
			`[data-comment-id="${commentId}"]`
		)
		const comment = commentCard.getAttribute('data-comment-content')
		const form = commentEdit.querySelector('form')
		commentEditComment.value = comment
		form.action = `/comment/edit/${commentId}`
		document.body.classList.add('no-scroll')
		commentEdit.showModal()
	})
})

commentEditClose.addEventListener('click', () => {
	closeModal()
})
