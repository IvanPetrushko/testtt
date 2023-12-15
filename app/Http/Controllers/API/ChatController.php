<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Chat;
use Illuminate\Http\JsonResponse;

class ChatController extends Controller
{
    public function get()
    {
        $chats = Chat::all();

        return $chats->map(function($chat, $key) {
            return [
                'chat_id' => $chat->chat_id,
                'enable_notification' => $chat->enable_notification,
            ];
        });
    }

    public function store(): JsonResponse
    {

        $validated = request()->validate([
            'chat_id' => ['required', 'numeric'],
            'enable_notification' =>['required', 'numeric']
        ]);

        $id = $validated['chat_id'];
        $enable_notification = $validated['enable_notification'];

        $item = [
            'chat_id'=>$id,
            'enable_notification'=>$enable_notification,
        ];

        Chat::create($item);

        return response()->json([
            'message' => 'success'
        ]);
    }


    public  function  update(int $id): JsonResponse
    {
        $validated = request()->validate([
            'enable_notification' =>['required', 'numeric']
        ]);

        $enable_notification = $validated['enable_notification'];

        $chat = Chat::where('chat_id', $id);
        $chat->update([
            'chat_id'=>$id,
            'enable_notification'=>$enable_notification,
        ]);

        return response()->json([
            'message' => 'success'
        ]);
    }
}
