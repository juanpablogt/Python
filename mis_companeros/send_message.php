<?php
require_once('../../config.php');

$courseid = required_param('courseid', PARAM_INT);
$selected_users = required_param_array('selected', PARAM_INT); // IDs de usuarios seleccionados
$message = required_param('message', PARAM_TEXT);

require_login($courseid);

$context = context_course::instance($courseid);
require_capability('block/mis_companeros:sendmessage', $context);

$PAGE->set_url('/blocks/mis_companeros/send_message.php', ['courseid' => $courseid]);

// Enviar mensajes a los usuarios seleccionados
$successful_sends = 0;
$failed_sends = 0;
foreach ($selected_users as $userid) {
    if (!$DB->record_exists('user', ['id' => $userid])) {
        debugging('User ID not found: ' . $userid);
        $failed_sends++;
        continue;
    }

    $user = $DB->get_record('user', ['id' => $userid], '*', MUST_EXIST);

    // Crear el mensaje
    $message_data = new \core\message\message();
    $message_data->component = 'moodle'; // Componente estándar
    $message_data->name = 'instantmessage'; // Tipo de mensaje
    $message_data->userfrom = $USER; // Usuario que envía el mensaje
    $message_data->userto = $user; // Usuario que recibe el mensaje
    $message_data->subject = get_string('newmessagefrom', 'block_mis_companeros', fullname($USER));
    $message_data->fullmessage = $message; // Contenido del mensaje
    $message_data->fullmessageformat = FORMAT_PLAIN; // Formato del mensaje
    $message_data->fullmessagehtml = ''; // Mensaje HTML vacío
    $message_data->smallmessage = ''; // Mensaje corto vacío
    $message_data->notification = 0; // Cambia a 1 si deseas que sea una notificación

    // Depuración de datos del mensaje
    debugging('Message data: ' . print_r($message_data, true));

    try {
        message_send($message_data); // Enviar el mensaje
        $successful_sends++;
    } catch (Exception $e) {
        debugging('Error sending message to user ID: ' . $userid . ' - ' . $e->getMessage());
        $failed_sends++;
    }
}

// Redireccionar al curso con un mensaje de éxito o error
if ($successful_sends > 0) {
    redirect(new moodle_url('/course/view.php', ['id' => $courseid]), get_string('messagesent', 'block_mis_companeros', $successful_sends), null, \core\output\notification::NOTIFY_SUCCESS);
} else {
    redirect(new moodle_url('/course/view.php', ['id' => $courseid]), get_string('messageerror', 'block_mis_companeros'), null, \core\output\notification::NOTIFY_ERROR);
}
