// window.dash_clientside = Object.assign({}, window.dash_clientside, {
//     clientside: {
//         show_feedback_form: function(_, dsn) {
//         Sentry.init({ dsn: dsn });
//         Sentry.captureMessage('Пользователь нажал кнопку Сообщить о проблеме, '.concat(window.performance.now()))
//         Sentry.showReportDialog({
//             lang: "ru",
//             title: "Обратная связь",
//             subtitle: "",
//             subtitle2: "",
//             labelName:	"Имя",
//             labelEmail:	"Эл. адрес",
//             labelComments: "Опишите проблему",
//             labelSubmit: "Отправить",
//             successMessage: "Ваш отзыв был отправлен. Благодарим вас!",
//             labelClose: "Закрыть",
//             errorFormEntry: "Не все поля корректно заполнены",
//             eventId: window.Sentry.lastEventId(),
//             onLoad: () => {
//                 const comments_input = document.getElementById("id_comments");
//                 comments_input && comments_input.setAttribute("placeholder","Описание проблемы");
//
//                 const name_input = document.getElementById("id_name");
//                 name_input && name_input.setAttribute("placeholder","Иван Ванко");
//
//                 const email_input = document.getElementById("id_email");
//                 email_input && email_input.setAttribute("placeholder","ivan_vanko@mail.gy");
//
//                 const powered_by = document.getElementsByClassName("powered-by");
//                 powered_by[0].innerText = ""
//                 }
//             })
//         }
// }   })
