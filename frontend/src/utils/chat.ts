export function formatChatTitle(fileName?: string) {
  if (!fileName) return 'Chat';

  const baseName = fileName.replace(/\.(txt|zip)$/i, '').trim();
  const match = baseName.match(/\bcon\s+(.+)$/i);
  const chatName = (match?.[1] ?? baseName).trim();

  return chatName ? `Chat con ${chatName}` : 'Chat';
}
