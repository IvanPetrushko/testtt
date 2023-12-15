<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\ChatMessage;
use Illuminate\Http\JsonResponse;

class ChatMessageController extends Controller
{
    public function get(): JsonResponse
    {
        $chatMessages = ChatMessage::all();

        $groupedData = [];

        foreach ($chatMessages as $item) {
            $group = $item["chat_id"];
            unset($item["chat_id"]);
            unset($item["id"]);
            $groupedData[$group][] = $item;
        }

        return response()->json($groupedData);
    }

    public function store(): JsonResponse
    {

        $validated = request()->validate([
            'chat_id' => ['required', 'numeric'],
            'message_id' => ['required', 'numeric'],
        ]);

        $id = $validated['chat_id'];
        $message_id = $validated['message_id'];

        $item = [
            'chat_id' => $id,
            'message_id' => $message_id,
        ];


        ChatMessage::create($item);

        return response()->json([
            'message' => 'success'
        ]);
    }

    public  function deleteMessage(int $id): JsonResponse
    {
        $message = ChatMessage::where('message_id', $id);
        $message->delete();
        return response()->json([
            'message' => 'success'
        ]);
    }

    public  function  deleteMessageByChat(int $id): JsonResponse
    {
        ChatMessage::where('chat_id', $id)->delete();

        return response()->json([
            'message' => 'success'
        ]);
    }

}
